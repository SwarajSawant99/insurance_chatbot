import json
import re


class SectionBuilder:
    def __init__(self, lines):
        self.lines = lines

    def is_noise(self, text):
        """
        Remove header/footer/company junk
        """
        noise_patterns = [
            r"www\.",
            r"customercare",
            r"toll free",
            r"onehealth",
            r"truth",
            r"must",
            r"be told",
            r"policy code",
            r"magma hdi",
            r"registered office"
        ]

        text_lower = text.lower()

        for pattern in noise_patterns:
            if re.search(pattern, text_lower):
                return True

        return False

    def is_heading(self, line):
        """
        Detect headings / sections
        """
        text = line["text"].strip()

        heading_patterns = [
            r"^section\s+\d+",
            r"^section\s+[ivxlc]+",
            r"^\d+\.\d+",
            r"^preamble$",
            r"^section i",
            r"^section ii",
            r"^section iii",
            r"^[A-Z\s\-–]+$"
        ]

        if line["font_size"] >= 11:
            return True

        for pattern in heading_patterns:
            if re.match(pattern, text.lower()):
                return True

        return False

    def is_definition(self, text):
        """
        Detect definitions
        """
        if ":" in text and len(text.split(":")[0].split()) <= 5:
            return True
        return False

    def build_sections(self):
        """
        Convert lines into logical sections
        """
        sections = []

        current_section = None
        current_content = []

        for line in self.lines:
            text = line["text"].strip()

            if not text:
                continue

            if self.is_noise(text):
                continue

            # heading found
            if self.is_heading(line):

                # save previous section
                if current_section:
                    current_section["content"] = " ".join(current_content).strip()
                    sections.append(current_section)

                current_section = {
                    "title": text,
                    "page_refs": [line["page"]],
                    "content": "",
                    "type": "section"
                }

                current_content = []

            else:
                if current_section:
                    current_content.append(text)

                    if line["page"] not in current_section["page_refs"]:
                        current_section["page_refs"].append(line["page"])

                else:
                    # create fallback section
                    current_section = {
                        "title": "General",
                        "page_refs": [line["page"]],
                        "content": "",
                        "type": "section"
                    }

                    current_content.append(text)

        # save last
        if current_section:
            current_section["content"] = " ".join(current_content).strip()
            sections.append(current_section)

        # second pass → detect definitions inside sections
        final_sections = []

        for sec in sections:
            content = sec["content"]

            definition_chunks = []

            lines_split = re.split(r'(?<=\.)\s+', content)

            temp_def = None
            temp_content = []

            for part in lines_split:
                if self.is_definition(part):

                    if temp_def:
                        definition_chunks.append({
                            "title": temp_def,
                            "content": " ".join(temp_content),
                            "page_refs": sec["page_refs"],
                            "type": "definition",
                            "parent": sec["title"]
                        })

                    key = part.split(":")[0].strip()
                    rest = ":".join(part.split(":")[1:]).strip()

                    temp_def = key
                    temp_content = [rest]

                else:
                    if temp_def:
                        temp_content.append(part)

            if temp_def:
                definition_chunks.append({
                    "title": temp_def,
                    "content": " ".join(temp_content),
                    "page_refs": sec["page_refs"],
                    "type": "definition",
                    "parent": sec["title"]
                })

            if definition_chunks:
                final_sections.extend(definition_chunks)
            else:
                final_sections.append(sec)

        return final_sections

    def save_to_json(self, output_path):
        sections = self.build_sections()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=4, ensure_ascii=False)

        print(f"Saved structured sections to {output_path}")