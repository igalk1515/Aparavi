# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system deps for camelot + PyMuPDF
RUN apt-get update && apt-get install -y sqlite3 \
    poppler-utils \
    ghostscript \
    libglib2.0-0 \
    libsm6 \
    libgl1  \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*


ENV PYTHONPATH="/app/src"

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Default command
CMD ["python", "src/run_etl.py"]
