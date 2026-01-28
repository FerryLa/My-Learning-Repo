import numpy as np
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

class EmbeddingBackend:
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name
        self._use_st = False
        self._tfidf = None
        try:
            if model_name:
                from sentence_transformers import SentenceTransformer
                self._st = SentenceTransformer(model_name)
                self._use_st = True
        except Exception:
            self._use_st = False

    def fit_corpus(self, texts: List[str]):
        if self._use_st:
            # sentence-transformers는 fit 불필요
            return
        self._tfidf = TfidfVectorizer(
            max_features=50000, ngram_range=(1,2), min_df=2
        )
        self._tfidf.fit(texts)

    def encode(self, texts: List[str]) -> np.ndarray:
        if self._use_st:
            arr = self._st.encode(texts, show_progress_bar=False, normalize_embeddings=True)
            return np.asarray(arr, dtype=np.float32)
        if self._tfidf is None:
            # 매우 작은 코퍼스에서도 돌아가게 안전장치
            self._tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1,2))
            self._tfidf.fit(texts)
        X = self._tfidf.transform(texts)
        X = normalize(X, norm="l2", copy=False)
        return X.toarray().astype(np.float32)
