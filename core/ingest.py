import os
from core.utils import chunk_text

class Ingestor:
    def __init__(self, embedder, db):
        self.embedder = embedder
        self.db = db

    def ingest(self, file_path):
        call_id = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            if not isinstance(chunk, str) or not chunk.strip():
                continue
            embedding = self.embedder.embed(chunk)
            metadata = {
                'call_id': call_id,
                'file_path': file_path,
                'chunk_index': idx,
                'text': chunk
            }
            self.db.add(embedding, metadata)
        return len(chunks)
