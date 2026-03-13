FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY ingest.py .
COPY test-frontend-backend.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY frontend /app/frontend
WORKDIR /app/frontend
RUN npm install

WORKDIR /app

ENV OLLAMA_BASE_URL=http://ollama:11435
ENV CHROMA_HOST=chroma
ENV CHROMA_PORT=8000
ENV FASTAPI_BASE_URL=http://localhost:8080
ENV FRONTEND_URL=http://localhost:3000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000 3000

ENTRYPOINT ["./entrypoint.sh"]
