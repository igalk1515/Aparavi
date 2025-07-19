# src/ingest/ocr_processor.py
"""
OCR processor for extracting text from PDF pages using Google Vision API and an API key.
"""

import os
import io
import base64
import requests
from PIL import Image


def run_ocr_with_google(pixmap) -> str:
    """
    Performs OCR on a PyMuPDF Pixmap using the Google Vision API with an API key.

    Args:
        pixmap: A PyMuPDF Pixmap object (rendered PDF page).

    Returns:
        Extracted text as a string.

    Raises:
        Exception if OCR fails or the API key is missing.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("❌ GOOGLE_API_KEY not found in environment variables.")

    # Convert Pixmap to PNG image bytes
    img_bytes = io.BytesIO(pixmap.tobytes("png"))

    # Encode image bytes to base64 for Vision API
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

    # Prepare Vision API request
    url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
    payload = {
        "requests": [{
            "image": {"content": img_base64},
            "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
        }]
    }

    response = requests.post(url, json=payload)

    # Parse response
    if response.status_code != 200:
        raise Exception(f"❌ Vision API error: {response.status_code} - {response.text}")

    result = response.json()
    try:
        return result["responses"][0]["fullTextAnnotation"]["text"]
    except (KeyError, IndexError):
        raise Exception(f"❌ No text found in Vision API response: {result}")
