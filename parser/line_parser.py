import json
from collections import defaultdict


class LineParser:
    def __init__(self, pdf_path):
        import fitz
        self.doc = fitz.open(pdf_path)

    def extract_lines(self):
        """
        Extract text at line level instead of block level
        """
        all_lines = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]

            page_dict = page.get_text("dict")

            lines_data = []

            for block in page_dict["blocks"]:
                if "lines" not in block:
                    continue

                for line in block["lines"]:
                    spans = []

                    for span in line["spans"]:
                        text = span["text"].strip()

                        if not text:
                            continue

                        spans.append({
                            "text": text,
                            "bbox": span["bbox"],
                            "font_size": span["size"],
                            "font_name": span["font"]
                        })

                    if not spans:
                        continue

                    # sort spans left to right
                    spans = sorted(spans, key=lambda s: s["bbox"][0])

                    merged_text = " ".join([s["text"] for s in spans])

                    x0 = min(s["bbox"][0] for s in spans)
                    y0 = min(s["bbox"][1] for s in spans)
                    x1 = max(s["bbox"][2] for s in spans)
                    y1 = max(s["bbox"][3] for s in spans)

                    avg_font = sum(s["font_size"] for s in spans) / len(spans)

                    lines_data.append({
                        "text": merged_text,
                        "page": page_num + 1,
                        "bbox": [x0, y0, x1, y1],
                        "font_size": round(avg_font, 2)
                    })

            # sort lines by y position
            lines_data = sorted(lines_data, key=lambda l: l["bbox"][1])

            all_lines.extend(lines_data)

        return all_lines

    def detect_columns_and_reorder(self, lines):
        """
        Better column reconstruction
        """
        final_lines = []

        pages = sorted(set(l["page"] for l in lines))

        for page in pages:
            page_lines = [l for l in lines if l["page"] == page]

            x_positions = [l["bbox"][0] for l in page_lines]
            page_width = max(l["bbox"][2] for l in page_lines)
            center = page_width / 2

            left = [l for l in page_lines if l["bbox"][0] < center]
            right = [l for l in page_lines if l["bbox"][0] >= center]

            # detect true two-column by number of lines
            if len(left) > 15 and len(right) > 15:
                layout = "two-column"

                left = sorted(left, key=lambda l: l["bbox"][1])
                right = sorted(right, key=lambda l: l["bbox"][1])

                ordered = left + right

            else:
                layout = "single"
                ordered = sorted(page_lines, key=lambda l: l["bbox"][1])

            print(f"Page {page}: {layout}")

            final_lines.extend(ordered)

        return final_lines

    def save_to_json(self, output_path):
        lines = self.extract_lines()
        ordered = self.detect_columns_and_reorder(lines)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(ordered, f, indent=4, ensure_ascii=False)

        print(f"Saved line-level structured output to {output_path}")