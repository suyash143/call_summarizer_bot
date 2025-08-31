# Handles retrieval of relevant transcript segments

class Retriever:
    def __init__(self, embedder, db):
        self.embedder = embedder
        self.db = db

    def retrieve(self, query, top_k=5):
        query_embedding = self.embedder.embed(query)
        results = self.db.search(query_embedding, top_k=top_k)
        print("HIGHLIGHTED RESULTS",)
        print("***********************"*20)
        print("Retrieved results:", results)
        return results

