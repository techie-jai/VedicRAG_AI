# Quick Start - Digital Nalanda

Get the complete Vedic RAG system running in one command.

## One-Command Startup

```bash
docker compose up
```

That's it! The system will:
- ✓ Start Ollama LLM server
- ✓ Download required models (gpt-oss:20b, nomic-embed-text)
- ✓ Start ChromaDB vector database
- ✓ Ingest scripture data automatically
- ✓ Start FastAPI backend on port 8080

## Access Points

Once running (wait for "Uvicorn running" message):

| Component | URL | Purpose |
|-----------|-----|---------|
| API Docs | http://localhost:8080/docs | Interactive API testing |
| Health Check | http://localhost:8080/health | System status |
| Frontend (optional) | http://localhost:3000 | Web UI |

## First Run Timeline

- **0-2 min**: Docker pulls images
- **2-5 min**: Ollama downloads models (first time only)
- **5-10 min**: ChromaDB starts and initializes
- **10-15 min**: Scripture data ingestion
- **Ready**: API available and responding

## Test the API

```bash
# Health check
curl http://localhost:8080/health

# Query example
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is dharma?"}'
```

## Frontend Setup (Optional)

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000

## Stop Everything

```bash
docker compose down
```

## Troubleshooting

**Services not starting?**
```bash
docker compose logs -f
```

**Out of memory?**
- Increase Docker memory allocation
- Or modify `entrypoint.sh` to use smaller model

**Models not downloading?**
```bash
docker exec ollama-server ollama pull gpt-oss:20b
docker exec ollama-server ollama pull nomic-embed-text
```

## What Changed

✅ **Ollama now runs in Docker** - No manual startup needed
✅ **Automatic model pulling** - Models download on first run
✅ **Automatic data ingestion** - Scriptures loaded on startup
✅ **Health checks** - Services wait for dependencies
✅ **Modern React UI** - Beautiful new frontend included
✅ **CORS enabled** - Frontend can communicate with backend

## Next Steps

1. Run `docker compose up`
2. Wait for startup complete
3. Visit http://localhost:8080/docs to test API
4. (Optional) Run frontend with `cd frontend && npm install && npm run dev`

See `DOCKER_SETUP.md` for detailed documentation.
