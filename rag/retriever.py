import faiss
import json
import pickle
from sentence_transformers import SentenceTransformer


# Load model ONLY ONCE
print("Loading embedding model...")
EMBEDDING_MODEL = SentenceTransformer(
    "paraphrase-MiniLM-L3-v2"
)
print("Embedding model loaded.")


class Retriever:

    def __init__(self, index_path, chunks_path):

        print(f"Loading index: {index_path}")

        # Reuse shared model
        self.model = EMBEDDING_MODEL

        # Load FAISS index
        self.index = faiss.read_index(index_path)

        # Load chunks
        if chunks_path.endswith(".json"):

            with open(
                chunks_path,
                "r",
                encoding="utf-8"
            ) as f:

                self.chunks = json.load(f)

        elif chunks_path.endswith(".pkl"):

            with open(
                chunks_path,
                "rb"
            ) as f:

                self.chunks = pickle.load(f)

        else:

            raise ValueError(
                "Unsupported chunks file format. Use .json or .pkl"
            )

        print(
            f"Loaded {len(self.chunks)} chunks from {chunks_path}"
        )

    def search(
        self,
        query,
        top_k=8
    ):

        print(f"Searching for: {query}")

        # Create query embedding
        query_embedding = self.model.encode(
            [query]
        )

        # Search FAISS
        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            chunk = self.chunks[idx]

            results.append({
                "score": float(score),
                "title": chunk.get(
                    "title",
                    "No Title"
                ),
                "content": chunk.get(
                    "content",
                    ""
                ),
                "page_refs": chunk.get(
                    "page_refs",
                    []
                )
            })

        print(
            f"Retrieved {len(results)} chunks"
        )

        return results