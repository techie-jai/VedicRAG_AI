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

# Start the FastAPI server in background
echo ""
echo "Starting Digital Nalanda API server..."
echo "Note: Data ingestion is now independent. Run 'docker exec <container> python ingest.py' to ingest data."
uvicorn main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait for FastAPI to be ready
echo ""
echo "Waiting for FastAPI to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo "✓ FastAPI is ready"
        break
    fi
    attempt=$((attempt + 1))
    echo "  Waiting... (attempt $attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ FastAPI failed to start within timeout"
    kill $FASTAPI_PID 2>/dev/null || true
    exit 1
fi

# Start the frontend dev server in background
echo ""
echo "Starting frontend development server..."
cd /app/frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to be ready
echo ""
echo "Waiting for frontend to be ready..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if curl -s http://127.0.0.1:3000 > /dev/null 2>&1; then
        echo "✓ Frontend is ready at http://localhost:3000"
        break
    fi
    attempt=$((attempt + 1))
    echo "  Waiting... (attempt $attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "✗ Frontend failed to start within timeout"
    kill $FASTAPI_PID $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

# Open the frontend in browser
echo ""
echo "Opening frontend in browser..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000 &
elif command -v open > /dev/null; then
    open http://localhost:3000 &
else
    echo "⚠ Could not open browser automatically. Visit http://localhost:3000 manually"
fi

# Run the test suite
echo ""
echo "Running Frontend & Backend Test Suite..."
cd /app
python test-frontend-backend.py

# Keep processes running
wait $FASTAPI_PID $FRONTEND_PID
