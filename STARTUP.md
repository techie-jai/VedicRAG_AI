# Digital Nalanda - Startup Guide

## Quick Start

### Option 1: Automated Startup (Recommended)
Run the startup script to automatically start all services and open the frontend:

```powershell
.\start.ps1
```

This will:
1. Start all Docker containers (Ollama, ChromaDB, FastAPI)
2. Wait for services to initialize
3. Open the frontend in your default browser at `http://localhost:3000`

### Option 2: Manual Startup

#### Step 1: Start Docker Containers
```powershell
docker compose up -d
```

#### Step 2: Start Frontend Development Server
```powershell
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend UI** | http://localhost:3000 | Web interface for querying Vedic scriptures |
| **Backend API** | http://localhost:8080 | FastAPI server (REST endpoints) |
| **Ollama** | http://localhost:11435 | LLM service (internal) |
| **ChromaDB** | http://localhost:8000 | Vector database (internal) |

## Frontend Features

- **Query Interface**: Ask questions about Vedic scriptures
- **Real-time Results**: Get answers with source citations
- **Health Monitoring**: View system status
- **Responsive Design**: Works on desktop and mobile

## Checking Service Status

```powershell
# View running containers
docker compose ps

# View logs
docker compose logs -f

# View specific service logs
docker compose logs nalanda-api
docker compose logs ollama-server
docker compose logs chroma-db
```

## Stopping Services

```powershell
# Stop all containers
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Troubleshooting

### Frontend not loading?
- Ensure backend is running: `curl http://localhost:8080/health`
- Check frontend dev server: `npm run dev` in the frontend directory
- Clear browser cache and refresh

### Backend connection error?
- Check if Docker containers are running: `docker compose ps`
- View backend logs: `docker compose logs nalanda-api`
- Ensure port 8080 is not in use: `netstat -ano | findstr "8080"`

### Ollama not responding?
- Check Ollama logs: `docker compose logs ollama-server`
- Verify port 11435 is available: `netstat -ano | findstr "11435"`

## Port Configuration

If ports are already in use, update `docker-compose.yml`:

```yaml
ports:
  - "YOUR_PORT:INTERNAL_PORT"
```

Then update the frontend `vite.config.js` proxy target accordingly.
