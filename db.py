import chromadb
import chromadb.config
import numpy as np
import uuid,os
from config import DEFAULT_CHROMA_COLLECTION, DEFAULT_CHROMA_PERSIST_DIR

# Handles vector DB and metadata storage using Chroma (persistent)

class DB:
    def __init__(self, collection_name=DEFAULT_CHROMA_COLLECTION, persist_directory=DEFAULT_CHROMA_PERSIST_DIR):
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)
        # Use PersistentClient instead of Client for persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(collection_name)
        self.persist_directory = persist_directory

    def add(self, embedding, metadata):
        """
        Add a new transcript segment embedding and its metadata to the vector DB.
        Required metadata schema:
            - call_id: str (unique identifier for the call)
            - file_path: str (path to transcript file)
            - chunk_index: int (index of the chunk in the file)
            - text: str (transcript segment)
            - speaker: str (optional, speaker name/role)
            - timestamp: str (optional, timestamp for the segment)
        """
        required_fields = ['call_id', 'file_path', 'chunk_index', 'text']
        for field in required_fields:
            if field not in metadata:
                raise ValueError(f"Missing required metadata field: {field}")
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

    def search(self, embedding, top_k=5, metadata_filter=None):
        """
        Retrieve the top_k most similar transcript segments to the given embedding.
        Optionally filter by metadata (e.g., call_id, file_path) to improve efficiency.
        Args:
            embedding: np.ndarray, the query embedding
            top_k: int, number of results to return
            metadata_filter: dict, optional, filter results by metadata fields
        Returns:
            List of metadata dicts with similarity scores
        """
        if embedding.ndim == 2:
            embedding = embedding[0]
        emb_list = embedding.tolist()
        query_args = {
            'query_embeddings': [emb_list],
            'n_results': top_k
        }
        if metadata_filter:
            query_args['where'] = metadata_filter
        results = self.collection.query(**query_args)
        out = []
        for i in range(len(results["ids"][0])):
            meta = dict(results["metadatas"][0][i])  # Ensure mutable dict
            meta["score"] = results["distances"][0][i]
            out.append(meta)
        return out

    def get_all_file_paths(self):
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
