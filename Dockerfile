FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY ingest.py .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV OLLAMA_BASE_URL=http://ollama:11434
ENV CHROMA_HOST=chroma
ENV CHROMA_PORT=8000
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
