from core.utils import chunk_text

class Ingestor:
    def __init__(self, embedder, db):
        self.embedder = embedder
        self.db = db

    def ingest(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        chunks = chunk_text(text)
        for idx, chunk in enumerate(chunks):
            embedding = self.embedder.embed(chunk)
            metadata = {
                'file_path': file_path,
                'chunk_index': idx,
                'text': chunk
            }
            self.db.add(embedding, metadata)
        return len(chunks)
