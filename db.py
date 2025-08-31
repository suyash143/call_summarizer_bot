import chromadb
import chromadb.config
import numpy as np
import uuid,os

# Handles vector DB and metadata storage using Chroma (persistent)

class DB:
    def __init__(self, collection_name="call_vectors", persist_directory="./chroma/"):
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)
        # Use PersistentClient instead of Client for persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.persist_directory = persist_directory

    def add(self, embedding, metadata):
        print(f"[DEBUG] add() called. persist_directory: {self.persist_directory}, collection_name: {self.collection.name}")
        print(f"[DEBUG] Adding embedding shape: {embedding.shape if hasattr(embedding, 'shape') else type(embedding)}, metadata: {metadata}")
        if embedding.ndim == 2:
            embedding = embedding[0]
        emb_list = embedding.tolist()
        doc_id = str(uuid.uuid4())
        self.collection.add(
            embeddings=[emb_list],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"[DEBUG] Document added with id: {doc_id}")

    def search(self, embedding, top_k=5):
        if embedding.ndim == 2:
            embedding = embedding[0]
        emb_list = embedding.tolist()
        results = self.collection.query(
            query_embeddings=[emb_list],
            n_results=top_k
        )
        out = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            meta["score"] = results["distances"][0][i]
            out.append(meta)
        return out

    def get_all_file_paths(self):
        # Chroma does not provide a direct way to get all metadatas, so we fetch all ids and then their metadatas
        all_ids = self.collection.get(ids=None)["ids"]
        file_paths = set()
        if all_ids:
            batch_size = 100
            for i in range(0, len(all_ids), batch_size):
                batch_ids = all_ids[i:i+batch_size]
                metadatas = self.collection.get(ids=batch_ids)["metadatas"]
                for meta in metadatas:
                    if meta and "file_path" in meta:
                        file_paths.add(meta["file_path"])
        return file_paths
