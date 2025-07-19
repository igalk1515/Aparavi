from transform.language_detector import detect_language

samples = [
    "This is a sample English invoice chunk.",
    "Dies ist ein deutscher Textauszug für eine Rechnung.",
    "This sentence contains both Deutsch und English mixed.",
    ""
]

for i, text in enumerate(samples):
    lang = detect_language(text)
    print(f"Chunk {i+1}: [{lang}] — {text[:60]}")
