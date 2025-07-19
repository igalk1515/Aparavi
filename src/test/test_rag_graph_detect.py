from graph.rag_graph import detect_query_language

def test_detect_language_node():
    state = {"query": "Was ist der Gesamtbetrag?"}
    result = detect_query_language(state)
    assert result["language"] in ("en", "de")
    print("✅ Detected:", result["language"])

if __name__ == "__main__":
    test_detect_language_node()
