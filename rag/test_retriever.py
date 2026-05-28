from retriever import Retriever

# health insurance retriever
retriever = Retriever(
    "output/health.index",
    "output/health_metadata.pkl"
)

query = "What is grace period?"

results = retriever.search(query)

for i, r in enumerate(results, 1):
    print(f"\nResult {i}")
    print("Score:", r["score"])
    print("Title:", r["title"])
    print("Pages:", r["page_refs"])
    print("Content:", r["content"][:500])