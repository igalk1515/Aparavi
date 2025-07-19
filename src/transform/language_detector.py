from langdetect import detect

def detect_language(text: str) -> str:
    """
    Detect the language of a given text chunk.
    
    Returns:
        "en" or "de" (default to "en" if detection fails or unknown)
    """
    try:
        lang = detect(text)
        return lang if lang in ("en", "de") else "en"
    except Exception:
        return "en"
