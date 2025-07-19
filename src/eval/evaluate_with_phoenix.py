# src/eval/evaluate_with_phoenix.py

import pandas as pd
import phoenix as px
from graph.rag_graph import build_rag_graph
from langgraph.graph import END

# Load CSV with ground truths
df = pd.read_csv("data/questions_with_partial_answers.csv")

rag = build_rag_graph()

records = []

for _, row in df.iterrows():
    question = row["question"]
    ground_truth = row["expected_answer"]

    # Run RAG pipeline
    state = rag.invoke({"query": question})

    predicted = state.get("answer")
    chunks = state.get("retrieved_chunks", [])

    context = "\n\n".join(
        f"(doc: {c.doc_id}, page: {c.page_num})\n{c.content[:300]}" for c in chunks
    )

    records.append({
        "question": question,
        "ground_truth": ground_truth,
        "predicted_answer": predicted,
        "context": context,
    })

eval_df = pd.DataFrame(records)

px.log(eval_df)

print("✅ Evaluation data sent to Arize Phoenix.")
