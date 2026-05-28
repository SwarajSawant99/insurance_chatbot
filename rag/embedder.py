import json
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_index(self, chunk_json_path, index_output, metadata_output):

        with open(chunk_json_path, "r", encoding="utf-8") as f:
            chunks = json.load(f)

        texts = []
        metadata = []

        for chunk in chunks:
            text = f"{chunk['title']} {chunk['content']}"

            texts.append(text)

            metadata.append({
                "chunk_id": chunk["chunk_id"],
                "title": chunk["title"],
                "content": chunk["content"],
                "page_refs": chunk["page_refs"],
                "parent": chunk.get("parent")
            })

        print(f"Creating embeddings for {len(texts)} chunks...")

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]

        # cosine similarity index
        index = faiss.IndexFlatIP(dimension)

        index.add(np.array(embeddings).astype("float32"))

        faiss.write_index(index, index_output)

        with open(metadata_output, "wb") as f:
            pickle.dump(metadata, f)

        print(f"Saved index: {index_output}")
        print(f"Saved metadata: {metadata_output}")