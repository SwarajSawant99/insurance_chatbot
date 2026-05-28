import os
from retriever import Retriever
from generator import GroqGenerator

API_KEY = "YOUR_GROQ_API_KEY"

# correct path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_PATH = os.path.join(BASE_DIR, "output", "health.index")
META_PATH = os.path.join(BASE_DIR, "output", "health_metadata.pkl")

retriever = Retriever(
    INDEX_PATH,
    META_PATH
)

generator = GroqGenerator(API_KEY)

query = "If my premium is overdue but still within grace period, will waiting period benefits continue and will I get hospitalization coverage?"

results = retriever.search(query)

answer = generator.generate_answer(query, results)

print("\nANSWER:\n")
print(answer)
