import numpy as np

def cosine_sim(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    # A: (n, d), B: (m, d), return (n, m)
    return A @ B.T

def mmr_select(cand_vecs, scores, k=50, lambda_=0.3):
    # cand_vecs: (n, d), scores: (n,)
    # 반환: 선택된 인덱스 리스트
    selected, rest = [], list(range(len(scores)))
    if len(rest) == 0:
        return selected
    # 첫 번째: 최고 점수
    best = int(np.argmax(scores))
    selected.append(best)
    rest.remove(best)

    while len(selected) < k and rest:
        sim_to_selected = np.max(cosine_sim(cand_vecs[rest], cand_vecs[selected]), axis=1)
        mmr_gain = lambda_ * scores[rest] - (1 - lambda_) * sim_to_selected
        pick = int(np.argmax(mmr_gain))
        selected_idx = rest[pick]
        selected.append(selected_idx)
        rest.pop(pick)
    return selected

def near_duplicate_drop(cand_vecs, picked_idx, history_vecs=None, thr=0.90):
    keep = []
    if history_vecs is None or len(history_vecs) == 0:
        return picked_idx
    for i in picked_idx:
        v = cand_vecs[i:i+1]
        sim = (v @ history_vecs.T).max()
        if sim < thr:
            keep.append(i)
    return keep
