from generate.response_generator import generate_answer
from retrieve.vector_retriever import search_vector

def test_generate_answer():
    chunks = search_vector("What is the invoice total?")
    answer = generate_answer("What is the invoice total?", chunks)
    print("✅ Answer:")
    print(answer)

if __name__ == "__main__":
    test_generate_answer()
