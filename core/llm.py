import requests
from sentence_transformers import SentenceTransformer
import numpy as np
from config.config import DEFAULT_EMBEDDING_MODEL, DEFAULT_LLM_BASE_URL, DEFAULT_LLM_MODEL

class Embedder:
    def __init__(self, model_name=DEFAULT_EMBEDDING_MODEL):
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        embedding = self.model.encode(text)
        return np.array(embedding, dtype=np.float32)

class LLM:
    def __init__(self, base_url=DEFAULT_LLM_BASE_URL, model=DEFAULT_LLM_MODEL):
        self.base_url = base_url
        self.model = model

    def ask(self, prompt):
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
