import faiss
import numpy as np

# Handles vector DB and metadata storage

class DB:
    def __init__(self):
        self.index = None  # Will be initialized on first add
        self.metadata = []  # List of dicts, one per embedding
        self.embedding_dim = None

    def add(self, embedding, metadata):
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        if self.index is None:
            self.embedding_dim = embedding.shape[1]
            self.index = faiss.IndexFlatL2(self.embedding_dim)
        elif embedding.shape[1] != self.embedding_dim:
            raise ValueError(f"Embedding dimension {embedding.shape[1]} does not match index dimension {self.embedding_dim}")
        self.index.add(embedding.astype(np.float32))
        self.metadata.append(metadata)

    def search(self, embedding, top_k=5):
        if self.index is None or self.index.ntotal == 0:
            return []
        if embedding.ndim == 1:
            embedding = embedding.reshape(1, -1)
        if embedding.shape[1] != self.embedding_dim:
            raise ValueError(f"Query embedding dimension {embedding.shape[1]} does not match index dimension {self.embedding_dim}")
        D, I = self.index.search(embedding.astype(np.float32), top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])
        return results
