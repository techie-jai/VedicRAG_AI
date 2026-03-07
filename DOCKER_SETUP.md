# Docker Setup Guide - Digital Nalanda

This guide explains the complete Docker setup for the Digital Nalanda Vedic RAG System.

## Overview

The application now runs completely in Docker with a single command:

```bash
docker compose up
```

This automatically:
1. Starts Ollama server with required models
2. Starts ChromaDB vector database
3. Ingests scripture data
4. Starts the FastAPI backend

## Architecture

### Services

**ollama** - LLM and Embedding Model Server
- Image: `ollama/ollama:latest`
- Port: `11434`
- Models: `gpt-oss:20b`, `nomic-embed-text`
- Healthcheck: API endpoint verification

**chroma** - Vector Database
- Image: `chromadb/chroma:latest`
- Port: `8000`
- Depends on: Ollama (healthy)
- Healthcheck: Heartbeat endpoint

**fastapi** - Backend API
- Built from local Dockerfile
- Port: `8080` (maps to 8000 internally)
- Depends on: ChromaDB (healthy)
- Automatically runs data ingestion on startup

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 8GB RAM available
- 10GB+ disk space for models and data

### Step 1: Start All Services

```bash
cd /path/to/Digital\ Nalanda
docker compose up
```

**First run takes 10-15 minutes** as it downloads:
- Ollama base image (~5GB)
- LLM model: gpt-oss:20b (~12GB)
- Embedding model: nomic-embed-text (~300MB)
- ChromaDB image

### Step 2: Wait for Startup

Watch the logs for:
```
nalanda-api | ✓ Models ready
nalanda-api | ✓ ChromaDB is ready
nalanda-api | Ingesting scripture data into ChromaDB...
nalanda-api | ✓ Data ingestion completed successfully
nalanda-api | Starting Digital Nalanda API server...
nalanda-api | Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Access the API

- **API Documentation**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health
- **Query Endpoint**: POST to http://localhost:8080/query

### Step 4: Run the Frontend (Optional)

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at `http://localhost:3000`

## Environment Variables

The following environment variables are automatically set:

```
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_HOST=chroma
CHROMA_PORT=8000
PYTHONUNBUFFERED=1
```

To override, create a `.env` file in the root directory:

```
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_HOST=chroma
CHROMA_PORT=8000
```

## Data Persistence

### Volumes

- **chroma_data**: Stores ChromaDB vector embeddings
- **ollama_data**: Stores downloaded models

These persist between container restarts.

### Scripture Data

The `./dharmaganj` directory is mounted as `/app/dharmaganj` in the container. The entrypoint script automatically ingests all `.txt` and `.md` files on startup.

## Troubleshooting

### Services Won't Start

**Check Docker daemon is running:**
```bash
docker ps
```

**View logs:**
```bash
docker compose logs -f
```

**Restart services:**
```bash
docker compose restart
```

### Out of Memory

The LLM model requires significant RAM. If you see OOM errors:

1. Increase Docker memory allocation (Docker Desktop settings)
2. Or use a smaller model by modifying the entrypoint.sh

### Models Not Downloading

If Ollama fails to pull models:

```bash
docker compose logs ollama
```

Models can be manually pulled:
```bash
docker exec ollama-server ollama pull gpt-oss:20b
docker exec ollama-server ollama pull nomic-embed-text
```

### ChromaDB Connection Issues

Ensure ChromaDB is healthy:
```bash
curl http://localhost:8000/api/v1/heartbeat
```

### API Not Responding

Check if FastAPI container is running:
```bash
docker compose logs fastapi
```

Verify health endpoint:
```bash
curl http://localhost:8080/health
```

## Development Workflow

### Modifying Backend Code

1. Edit `main.py` or `ingest.py`
2. Rebuild container: `docker compose build`
3. Restart: `docker compose up`

### Modifying Frontend Code

1. Edit files in `frontend/src/`
2. Changes auto-reload with `npm run dev`

### Adding New Scripture Data

1. Add `.txt` or `.md` files to `./dharmaganj/`
2. Restart FastAPI container: `docker compose restart fastapi`
3. Ingestion runs automatically

## Stopping Services

```bash
docker compose down
```

To also remove volumes:
```bash
docker compose down -v
```

## Performance Notes

- First query takes 30-60 seconds (model loading)
- Subsequent queries: 5-15 seconds
- Ingestion speed: ~100 documents per minute

## API Examples

### Health Check
```bash
curl http://localhost:8080/health
```

### Query Scriptures
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the meaning of dharma?"}'
```

### View API Docs
Open http://localhost:8080/docs in browser

## Production Deployment

For production:

1. Use specific image versions instead of `latest`
2. Set resource limits in docker-compose.yml
3. Configure proper logging
4. Use environment-specific .env files
5. Set up health checks and monitoring
6. Use a reverse proxy (nginx) for the frontend

## Support

For issues or questions, check:
- Docker logs: `docker compose logs`
- API documentation: http://localhost:8080/docs
- Health status: http://localhost:8080/health
