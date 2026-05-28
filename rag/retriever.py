import faiss
import json
import pickle
from sentence_transformers import SentenceTransformer


class Retriever:
    def __init__(self, index_path, chunks_path):
        print("Loading retriever...")

        # embedding model
        self.model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

        # load faiss index
        self.index = faiss.read_index(index_path)

        # load chunks file
        if chunks_path.endswith(".json"):
            with open(chunks_path, "r", encoding="utf-8") as f:
                self.chunks = json.load(f)

        elif chunks_path.endswith(".pkl"):
            with open(chunks_path, "rb") as f:
                self.chunks = pickle.load(f)

        else:
            raise ValueError("Unsupported chunks file format. Use .json or .pkl")

    def search(self, query, top_k=8):
        # create query embedding
        query_embedding = self.model.encode([query])

        # search FAISS
        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            chunk = self.chunks[idx]

            results.append({
                "score": float(score),
                "title": chunk.get("title", "No Title"),
                "content": chunk.get("content", ""),
                "page_refs": chunk.get("page_refs", [])
            })

        return results