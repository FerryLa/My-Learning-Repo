import argparse, os, yaml, hashlib
import pandas as pd
import numpy as np
from tqdm import tqdm
from .crawl_rss import crawl_feeds
from .extract_text import extract
from .embed import EmbeddingBackend
from .similarity import cosine_sim, mmr_select, near_duplicate_drop
from .enex_prototypes import build_prototypes
from .telegram_client import send_message

def normalize_url(u: str) -> str:
    # extremely simple normalization; extend as needed
    return u.split("#")[0].split("?")[0].strip().lower()

def summarize(text: str, max_chars: int = 280) -> str:
    # naive summary: first 2 lines trimmed. Replace with better summarizer later.
    lines = [ln.strip() for ln in text.splitlines() if len(ln.strip()) > 0]
    s = " ".join(lines[:3])
    if len(s) > max_chars:
        s = s[:max_chars].rsplit(" ", 1)[0] + "…"
    return s

def main(cfg):
    os.makedirs(cfg.get("outbox_dir", "./outbox"), exist_ok=True)

    # 1) prototypes from ENEX
    protos, _ = build_prototypes(cfg["data_csv"], model_name=None, k=30)

    # 2) fetch candidates from RSS
    feeds = cfg.get("rss_feeds", [])
    cands = crawl_feeds(feeds, limit=cfg.get("max_candidates", 800))

    # normalize URLs and drop dups
    seen = set()
    uniq = []
    for x in cands:
        u = normalize_url(x["url"])
        if u and u not in seen:
            seen.add(u)
            uniq.append(x)
    cands = uniq

    # 3) extract text
    for x in tqdm(cands, desc="extract_text"):
        info = extract(x["url"])
        x["ok"] = info["ok"]
        x["text"] = info["text"]
    cands = [x for x in cands if x.get("ok") and len(x.get("text","")) > 120]

    if not cands:
        print("no candidates with text")
        return

    # 4) embedding
    emb = EmbeddingBackend(model_name=None)
    emb.fit_corpus([x["text"] for x in cands])
    cand_vecs = emb.encode([x["text"] for x in cands])

    # 5) similarity to prototypes
    S = cosine_sim(cand_vecs, protos)        # (N, K)
    best = S.max(axis=1)
    keep_idx = np.where(best >= cfg.get("min_similarity", 0.62))[0]

    # 6) diversity with MMR and per-topic cap
    kept_vecs = cand_vecs[keep_idx]
    kept_scores = best[keep_idx]
    mmr_idx_local = mmr_select(kept_vecs, kept_scores, k=200, lambda_=cfg.get("mmr_lambda", 0.3))
    picked_idx = [keep_idx[i] for i in mmr_idx_local]

    # TODO: near-duplicate with history vectors (out of scope here)
    # picked_idx = near_duplicate_drop(cand_vecs, picked_idx, history_vecs, thr=0.90)

    # 7) format and send (cap by send_limit)
    send_ct = 0
    limit = cfg.get("send_limit", 60)
    for i in picked_idx:
        x = cands[i]
        title = x["title"] or "(제목 없음)"
        summ = summarize(x["text"])
        url = x["url"]
        msg = f"<b>{title}</b>\n{summ}\n\n원문: {url}"
        send_message(msg, disable_preview=False)
        send_ct += 1
        if send_ct >= limit:
            break

    # 8) save local record
    out_csv = os.path.join(cfg.get("outbox_dir","./outbox"), "sent_log.csv")
    df = pd.DataFrame([cands[i] for i in picked_idx][:limit])
    df.to_csv(out_csv, index=False)
    print("sent:", send_ct, "saved log:", out_csv)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    with open(args.config, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    main(cfg)
