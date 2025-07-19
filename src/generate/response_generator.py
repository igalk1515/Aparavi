# src/generate/response_generator.py

from openai import OpenAI
from models.data_models import ContentChunk
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(query: str, chunks: list[ContentChunk]) -> str:
    context = ""
    for chunk in chunks:
        source = f"(doc: {chunk.doc_id}, page: {chunk.page_num})"
        context += f"{source}\n{chunk.content}\n\n"

    prompt = (
        "You are a helpful assistant. Use the following document snippets to answer the question.\n"
        "Always cite the document ID and page number when answering.\n\n"
        f"Context:\n{context}\n"
        f"Question: {query}\n"
        "Answer:"
    )

    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-4o"
        messages=[
            {"role": "system", "content": "You are an intelligent document QA agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
