from groq import Groq
import time


class GroqGenerator:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)

    def generate_answer(self, query, retrieved_chunks):
        context = ""

        for i, chunk in enumerate(retrieved_chunks, 1):
            context += f"""
Chunk {i}
Title: {chunk['title']}
Pages: {chunk['page_refs']}
Content: {chunk['content']}

"""

        prompt = f"""
You are an expert insurance policy assistant.

Your job is to answer ONLY using the provided policy document context.

IMPORTANT RULES:

1. Use ALL chunks and combine information from multiple chunks if needed.
2. Do NOT answer using only one chunk if the question involves multiple conditions.
3. If one clause affects another clause, explain both clearly.
4. Mention conditions, exclusions, waiting periods, exceptions if applicable.
5. Answer in simple human language.
6. Mention page numbers in your answer.
7. Do NOT say "This information is not available in the policy document"
   unless absolutely no relevant context exists.
8. If answer is conditional, explain like:
   - If X → then Y
   - However if Z → then A

User Question:
{query}

Policy Context:
{context}

Give answer in this format:

- Clear explanation
- Conditions/exceptions if any
- Mention page numbers
"""

        # retry logic
        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are an insurance document reasoning assistant.

You must combine evidence from multiple chunks before answering.

Never ignore relevant chunks.
Never prematurely say information is unavailable.
Always explain exceptions and conditions.
"""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1   # lower = more factual
                )

                return response.choices[0].message.content

            except Exception as e:
                print(f"Groq failed (attempt {attempt+1}): {e}")
                time.sleep(3)

        # fallback if Groq fails
        best_chunk = retrieved_chunks[0]

        fallback_answer = f"""
Groq service temporarily unavailable.

Best matching answer from policy document:

Title: {best_chunk['title']}
Pages: {best_chunk['page_refs']}

Answer:
{best_chunk['content']}
"""

        return fallback_answer