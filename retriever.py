# Handles retrieval of relevant transcript segments

class Retriever:
    def __init__(self, embedder, db):
        self.embedder = embedder
        self.db = db

    def retrieve(self, query, top_k=5, metadata_filter=None):
        """
        Retrieve relevant transcript segments for a query.
        Optional filter by metadata
        """
        query_embedding = self.embedder.embed(query)
        results = self.db.search(query_embedding, top_k=top_k, metadata_filter=metadata_filter)
        return results
