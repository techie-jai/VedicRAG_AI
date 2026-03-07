# Deployment Summary - Digital Nalanda

## Problem Solved

**Original Issue**: `docker compose up` didn't start the application because:
- Ollama server had to be started manually
- No orchestration between services
- Data ingestion was a separate manual step
- No modern UI included

**Solution Implemented**: Complete Docker orchestration with automatic startup

## What Was Changed

### 1. Docker Compose (`docker-compose.yml`)
- **Added Ollama service** with health checks
- **Added service dependencies** with health conditions
- **Updated environment variables** for Docker networking
- **Added volume persistence** for models and data
- **Removed host.docker.internal** references (not needed)

### 2. Dockerfile
- **Added entrypoint script** for orchestration
- **Updated environment variables** to use Docker DNS
- **Removed direct CMD** in favor of entrypoint

### 3. Entrypoint Script (`entrypoint.sh`)
Handles startup sequence:
1. Waits for Ollama to be ready
2. Pulls required models (gpt-oss:20b, nomic-embed-text)
3. Waits for ChromaDB to be ready
4. Runs data ingestion automatically
5. Starts FastAPI server

### 4. Backend Updates
- **main.py**: Added CORS middleware for frontend communication
- **ingest.py**: Updated default port to 8000 (Docker standard)

### 5. Modern React Frontend
Complete new UI with:
- Real-time query interface
- Source citation display
- System health monitoring
- Responsive design
- Built with React, Tailwind CSS, Lucide icons

## File Structure

```
Digital Nalanda/
├── docker-compose.yml          (Updated: Ollama + health checks)
├── Dockerfile                  (Updated: entrypoint support)
├── entrypoint.sh              (New: startup orchestration)
├── main.py                    (Updated: CORS middleware)
├── ingest.py                  (Updated: port config)
├── QUICK_START.md             (New: quick reference)
├── DOCKER_SETUP.md            (New: detailed guide)
├── DEPLOYMENT_SUMMARY.md      (This file)
└── frontend/                  (New: React UI)
    ├── package.json
    ├── index.html
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    ├── .env.example
    └── src/
        ├── main.jsx
        ├── index.css
        ├── App.jsx
        └── components/
            ├── QueryInterface.jsx
            ├── SourceCard.jsx
            ├── Header.jsx
            └── HealthStatus.jsx
```

## How It Works Now

### Single Command Startup
```bash
docker compose up
```

### Automatic Sequence
1. **Ollama Service Starts**
   - Listens on port 11434
   - Health check verifies API availability

2. **ChromaDB Waits for Ollama**
   - Starts only after Ollama is healthy
   - Listens on port 8000
   - Health check verifies heartbeat

3. **FastAPI Waits for ChromaDB**
   - Starts only after ChromaDB is healthy
   - Runs entrypoint.sh which:
     - Pulls models from Ollama
     - Ingests scripture data
     - Starts API server on port 8080

4. **Frontend (Optional)**
   - Run separately: `cd frontend && npm install && npm run dev`
   - Connects to API at http://localhost:8080
   - Available at http://localhost:3000

## Key Improvements

| Before | After |
|--------|-------|
| Manual Ollama startup | Automatic in Docker |
| Manual data ingestion | Automatic on startup |
| Streamlit UI only | Modern React UI included |
| No service coordination | Health checks + dependencies |
| No CORS support | CORS enabled for frontend |
| Port conflicts | Properly mapped ports |

## Ports

| Service | Port | Purpose |
|---------|------|---------|
| Ollama | 11434 | LLM & embeddings (internal) |
| ChromaDB | 8000 | Vector DB (internal) |
| FastAPI | 8080 | Backend API (external) |
| Frontend | 3000 | Web UI (optional) |

## Environment Variables

Automatically set in Docker:
```
OLLAMA_BASE_URL=http://ollama:11434
CHROMA_HOST=chroma
CHROMA_PORT=8000
PYTHONUNBUFFERED=1
```

## First Run Expectations

- **Total time**: 10-15 minutes
- **Downloads**: ~17GB (models + images)
- **Disk space needed**: 20GB+
- **RAM needed**: 8GB minimum

## Testing

### API Health
```bash
curl http://localhost:8080/health
```

### Query Example
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is dharma?"}'
```

### API Documentation
Visit: http://localhost:8080/docs

## Troubleshooting

See `DOCKER_SETUP.md` for detailed troubleshooting guide.

Quick fixes:
- View logs: `docker compose logs -f`
- Restart: `docker compose restart`
- Rebuild: `docker compose build && docker compose up`
- Clean: `docker compose down -v`

## Next Steps

1. Run `docker compose up`
2. Wait for "Uvicorn running" message
3. Test API at http://localhost:8080/docs
4. (Optional) Run frontend with npm

## Documentation

- **QUICK_START.md**: Get running in 5 minutes
- **DOCKER_SETUP.md**: Complete technical guide
- **DEPLOYMENT_SUMMARY.md**: This file - what changed and why
