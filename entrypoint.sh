#!/bin/bash
set -e

echo "=========================================="
echo "Digital Nalanda - Startup Orchestration"
echo "=========================================="

# Wait for Ollama to be ready and pull required models
echo "Waiting for Ollama service to be ready..."
max_attempts=60
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if python -c "import urllib.request; urllib.request.urlopen('http://ollama:11435/api/tags')" > /dev/null 2>&1; then
        echo "✓ Ollama is ready"
        break
    fi
    attempt=$((attempt + 1))
    echo "  Waiting... (attempt $attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ Ollama failed to start within timeout"
    exit 1
fi

# Verify required models are available
echo ""
echo "Verifying Ollama models..."
MODELS=$(python -c "import urllib.request, json; data=json.loads(urllib.request.urlopen('http://ollama:11435/api/tags').read()); print('\\n'.join([m['name'] for m in data.get('models', [])]))" 2>/dev/null || echo "")

if echo "$MODELS" | grep -q "gpt-oss"; then
    echo "✓ gpt-oss:20b model found"
else
    echo "  Pulling gpt-oss:20b (LLM)..."
    ollama pull gpt-oss:20b || echo "  Warning: Could not pull gpt-oss:20b"
fi

if echo "$MODELS" | grep -q "nomic-embed-text"; then
    echo "✓ nomic-embed-text model found"
else
    echo "  Pulling nomic-embed-text (Embeddings)..."
    ollama pull nomic-embed-text || echo "  Warning: Could not pull nomic-embed-text"
fi

echo "✓ Models ready"

# Wait for ChromaDB to be ready
echo ""
echo "Waiting for ChromaDB to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if python -c "import socket; socket.create_connection(('chroma', 8000), timeout=2)" > /dev/null 2>&1; then
        echo "✓ ChromaDB is ready"
        break
    fi
    attempt=$((attempt + 1))
    echo "  Waiting... (attempt $attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ ChromaDB failed to start within timeout"
    exit 1
fi

# Start the FastAPI server
echo ""
echo "Starting Digital Nalanda API server..."
echo "Note: Data ingestion is now independent. Run 'docker exec <container> python ingest.py' to ingest data."
exec uvicorn main:app --host 0.0.0.0 --port 8000
