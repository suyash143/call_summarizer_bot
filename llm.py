import requests
from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, text):
        embedding = self.model.encode(text)
        return np.array(embedding, dtype=np.float32)

class LLM:
    def __init__(self, base_url="http://192.168.29.17:11434/api/generate", model="llama2:7b-chat-q4_0"):
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

