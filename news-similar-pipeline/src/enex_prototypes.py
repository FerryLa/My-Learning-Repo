import pandas as pd
import numpy as np
from typing import Tuple, List
from .embed import EmbeddingBackend

def build_prototypes(enex_csv: str, model_name: str = None, k: int = 30) -> Tuple[np.ndarray, List[int]]:
    df = pd.read_csv(enex_csv)
    texts = (df["text"].fillna("").astype(str)).tolist()
    texts = [t for t in texts if len(t.strip()) > 40]
    if len(texts) < 20:
        k = max(5, len(texts)//2 or 1)

    emb = EmbeddingBackend(model_name=model_name)
    emb.fit_corpus(texts)
    vecs = emb.encode(texts)

    # simple kmeans via sklearn
    from sklearn.cluster import KMeans
    k = min(k, max(1, len(texts)//20 or 1))
    km = KMeans(n_clusters=k, n_init=5, random_state=42).fit(vecs)
    labels = km.labels_

    protos = []
    for cid in range(k):
        m = vecs[labels == cid].mean(axis=0, keepdims=True)
        protos.append(m)
    protos = np.vstack(protos)
    # L2 normalize prototypes
    protos /= (np.linalg.norm(protos, axis=1, keepdims=True) + 1e-9)
    return protos, labels.tolist()
