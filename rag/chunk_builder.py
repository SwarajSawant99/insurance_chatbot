import json
import uuid


class ChunkBuilder:
    def __init__(self, sections):
        self.sections = sections

    def make_chunk(self, title, content, pages, parent=None):
        return {
            "chunk_id": str(uuid.uuid4()),
            "title": title,
            "parent": parent,
            "content": content,
            "page_refs": pages
        }

    def split_large_content(self, text, max_words=250):
        words = text.split()

        if len(words) <= max_words:
            return [text]

        chunks = []
        current = []

        for word in words:
            current.append(word)

            if len(current) >= max_words:
                chunks.append(" ".join(current))
                current = []

        if current:
            chunks.append(" ".join(current))

        return chunks

    def build_chunks(self):
        final_chunks = []

        for sec in self.sections:
            title = sec.get("title", "Untitled")
            content = sec.get("content", "")
            pages = sec.get("page_refs", [])
            parent = sec.get("parent", None)

            if not content.strip():
                continue

            split_chunks = self.split_large_content(content)

            for idx, piece in enumerate(split_chunks):
                chunk_title = title

                if len(split_chunks) > 1:
                    chunk_title = f"{title} (Part {idx+1})"

                final_chunks.append(
                    self.make_chunk(
                        title=chunk_title,
                        content=piece,
                        pages=pages,
                        parent=parent
                    )
                )

        return final_chunks

    def save_to_json(self, output_path):
        chunks = self.build_chunks()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=4, ensure_ascii=False)

        print(f"Saved chunks to {output_path}")