# Digital Nalanda Frontend

Modern React-based UI for the Digital Nalanda Vedic RAG System.

## Features

- **Real-time Query Interface**: Ask questions about Vedic scriptures
- **Source Citations**: Every answer includes references to original texts
- **Health Monitoring**: Real-time system status display
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Built with React, Tailwind CSS, and Lucide icons

## Setup

### Prerequisites
- Node.js 16+ and npm

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

## Configuration

Create a `.env` file based on `.env.example`:

```
VITE_API_URL=http://localhost:8080
```

## API Integration

The frontend communicates with the FastAPI backend at the configured `VITE_API_URL`. Ensure the backend is running before starting the frontend.

### API Endpoints Used

- `GET /health` - System health check
- `POST /query` - Submit a query to the RAG system

## Architecture

- **App.jsx**: Main application component with message management
- **QueryInterface**: Input form for scripture queries
- **SourceCard**: Displays source citations
- **Header**: Application header with branding
- **HealthStatus**: Real-time system status indicator
