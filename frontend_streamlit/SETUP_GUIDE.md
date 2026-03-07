# Digital Nalanda Frontend - Setup & Connection Guide

## Status: ✅ FULLY OPERATIONAL

The frontend is now fully connected to the backend RAG system with all issues resolved.

## What Was Fixed

### 1. Text Overlapping Issues
- **Removed all emoji/icon elements** that were causing text overlap in the UI
- Added proper `line-height: 1.6` to all text elements
- Increased padding and margins in chat messages
- Implemented `word-wrap: break-word` for proper text wrapping

### 2. Bhagwa (Saffron) Color Theme
- Replaced all gold accents with Bhagwa color (#FF9933)
- Updated primary theme color in Streamlit config
- Applied saffron color to:
  - Sidebar borders (3px solid)
  - Headings (h2, h3)
  - Button gradients
  - Input field borders
  - Expander buttons
  - Source item borders
  - Confidence badges

### 3. Backend Integration
- Created `api_client.py` module for backend API communication
- Updated `main.py` to use actual backend responses instead of mock data
- Configured backend URL to `http://localhost:8080` (Docker port mapping)
- Increased request timeout to 120 seconds for LLM inference

## Current Setup

### Running Services
- **Frontend**: Streamlit on `http://localhost:8503`
- **Backend API**: FastAPI on `http://localhost:8080` (Docker container: nalanda-api)
- **Vector DB**: ChromaDB on `http://localhost:8000` (Docker container: chroma-db)
- **LLM**: Ollama on `http://localhost:11434` (Host machine)

### Data Status
- ✅ 5 scripture documents loaded
- ✅ 35 chunks created and embedded
- ✅ Data successfully ingested into ChromaDB
- ✅ Backend can process queries and retrieve sources

## Testing the Connection

Run the connection test script:
```bash
cd "e:\25. Codes\12. Vedic RAG AI\Code Workspace\frontend_streamlit"
python test_backend_connection.py
```

Expected output:
```
1. Checking backend health...
   Status: HEALTHY

2. Getting detailed backend status...
   Status: {healthy, service info, etc.}

3. Testing a sample query...
   Query: What is Brahman according to Vedanta?
   Status: SUCCESS
   Answer: [Retrieved from scriptures]
   Sources found: 2
   Confidence: 85%
```

## Using the Frontend

1. **Start the Frontend** (if not already running):
   ```bash
   cd "e:\25. Codes\12. Vedic RAG AI\Code Workspace\frontend_streamlit"
   streamlit run main.py
   ```

2. **Access the App**:
   - Open browser to `http://localhost:8503`
   - Or use the Streamlit URL provided in terminal

3. **Features Available**:
   - **Chat Interface**: Ask questions about scriptures
   - **Sample Questions**: Click pre-loaded questions for quick exploration
   - **Sources Expander**: View retrieved text chunks with confidence scores
   - **Researcher Mode**: Toggle in sidebar for detailed scholarly information
   - **Backend Status**: Real-time backend health indicator in sidebar
   - **Browse Scriptures**: Category-based scripture exploration

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│              (http://localhost:8503)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Chat Interface                                     │  │
│  │ • Sample Questions Grid                             │  │
│  │ • Sources & Confidence Display                      │  │
│  │ • Researcher Mode Toggle                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↓
                    api_client.py
                   (HTTP Requests)
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Docker)                    │
│              (http://localhost:8080)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Query Processing                                   │  │
│  │ • RAG Pipeline (Retrieval + Generation)             │  │
│  │ • Source Extraction                                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
         ↓                                    ↓
    ChromaDB                              Ollama LLM
  (Vector DB)                          (Language Model)
  localhost:8000                      localhost:11434
```

## File Structure

```
frontend_streamlit/
├── main.py                          # Main Streamlit application
├── api_client.py                    # Backend API integration
├── test_backend_connection.py       # Connection test script
├── requirements.txt                 # Python dependencies
├── .streamlit/
│   └── config.toml                  # Streamlit theme configuration
├── README.md                        # User documentation
└── SETUP_GUIDE.md                   # This file
```

## Configuration

### Environment Variables
You can override the backend URL by setting:
```bash
set BACKEND_URL=http://your-backend-url:port
```

### Streamlit Config
Edit `.streamlit/config.toml` to customize:
- Theme colors
- Primary color: `#FF9933` (Bhagwa)
- Background: `#1a1a1a` (Deep Charcoal)
- Secondary background: `#2d2d2d`
- Text color: `#F5F5F5` (Off-white)

## Troubleshooting

### Backend Connection Issues
1. Check if Docker containers are running:
   ```bash
   docker ps
   ```
   Should show: `nalanda-api`, `chroma-db`

2. Verify Ollama is running:
   ```bash
   Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing
   ```

3. Check backend logs:
   ```bash
   docker logs nalanda-api
   ```

### Slow Responses
- LLM inference can take 30-120 seconds depending on query complexity
- Timeout is set to 120 seconds in `api_client.py`
- Increase if needed for slower systems

### No Sources Displayed
- Ensure data has been ingested: `docker exec nalanda-api python ingest.py`
- Check ChromaDB collection has data
- Verify query matches indexed documents

## Performance Notes

- **First Query**: May take 60-120 seconds (LLM warmup)
- **Subsequent Queries**: 30-60 seconds (cached embeddings)
- **Memory Usage**: ~4GB for LLM + embeddings
- **Recommended**: Run on system with 8GB+ RAM

## Next Steps

1. ✅ Frontend is running and connected
2. ✅ Backend is processing queries
3. ✅ Data is indexed and searchable
4. **Optional**: Add more scripture documents to `Docker Code/data/` and re-run ingest
5. **Optional**: Fine-tune LLM parameters in backend `main.py`
6. **Optional**: Customize sample questions in frontend `main.py`

## Support

For issues or questions:
1. Check backend logs: `docker logs nalanda-api`
2. Run connection test: `python test_backend_connection.py`
3. Verify all Docker containers are running: `docker ps`
4. Check Ollama availability: `http://localhost:11434/api/tags`

---

**Digital Nalanda v1.0.0** - Exploring Ancient Wisdom Through Modern AI
