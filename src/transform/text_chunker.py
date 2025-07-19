# text_chunker.py
def chunk_text(text: str, max_tokens: int = 300) -> list[str]:
    """
    Splits the input text into chunks of approximately `max_tokens` words.
    This is a simple word-count approximation (not token-aware).
    
    Args:
        text (str): Raw extracted text
        max_tokens (int): Approximate max words per chunk

    Returns:
        list[str]: List of text chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i + max_tokens])
        chunks.append(chunk)

    return chunks
