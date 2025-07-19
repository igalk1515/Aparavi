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

    prompt = f"""
You are a multilingual assistant answering questions using the document snippets below. Each snippet is labeled with a document ID and page number.

Document Type: Invoices
Snippets may include:
- Invoice metadata (Invoice Number, Invoice Date, Due Date)
- Buyer and seller information (Sold-To, Billed-To)
- Itemized charges with service periods
- Totals, VAT, credits, payment instructions

Instructions:
- Answer **only** using the snippets below.
- If multiple totals exist, choose the **most recent or relevant** one.
- If no answer can be found, reply: "The total is not available in the provided context."
- Reply in the **same language** as the user's question.
- Always cite source like this: (doc: ..., page: ...)

Snippets:
{context}

Question: {query}

Answer:
""".strip()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an intelligent document QA agent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
