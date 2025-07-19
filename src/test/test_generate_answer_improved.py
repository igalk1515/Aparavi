from retrieve.hybrid_retriever import hybrid_search
from generate.response_generator import generate_answer

query = "What is the invoice total?"

# Run hybrid retrieval (vector + SQL)
chunks = hybrid_search(query)

# Generate answer with citations
answer = generate_answer(query, chunks)

print("\n✅ Final Answer:\n")
print(answer)
