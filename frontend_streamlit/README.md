# Digital Nalanda - Streamlit Frontend

A professional, sleek, and modern Streamlit-based frontend for the Digital Nalanda RAG system. This interface provides access to ancient Indian scriptures through an intuitive chat interface with advanced retrieval features.

## Features

### 🎨 Design & UX
- **Premium Academic Aesthetic**: Dark theme with gold accents reflecting scholarly elegance
- **Responsive Layout**: Wide-page layout with collapsible sidebar navigation
- **Custom Typography**: Serif fonts for headings (Crimson Text) and sans-serif for body (Inter)
- **Color Palette**:
  - Deep Charcoal: `#1a1a1a` (primary background)
  - Gold: `#D4AF37` (accents and highlights)
  - Off-White: `#F5F5F5` (text)
  - Secondary Dark: `#2d2d2d` (secondary backgrounds)

### 💬 Chat Interface
- Full conversation history with message persistence
- User and assistant message differentiation with visual styling
- Real-time message streaming support
- Pinned input field at bottom of screen

### 📚 RAG Features
- **Sources Expander**: View specific verses and text chunks retrieved from Vector DB
- **Confidence Scores**: Relevance metrics for each retrieved source
- **Sanskrit Display**: Original Sanskrit shlokas with transliteration
- **Scholarly Commentaries**: Links and references to classical commentaries (Shankara Bhashya, etc.)

### 🔬 Researcher Mode
- Toggle in sidebar for detailed scholarly information
- Shows original Sanskrit shlokas and transliteration
- Displays multiple scholarly commentary references
- Ideal for academic research and deep exploration

### 🧭 Navigation
- **Chat**: Main interface for querying scriptures
- **Browse Scriptures**: Category-based scripture exploration
- **About**: Project information and technology stack

### 💡 Sample Questions
- Pre-populated grid of common questions
- Click-to-query functionality for new users
- Covers major philosophical concepts

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Setup Steps

1. **Navigate to the frontend directory:**
   ```bash
   cd "e:\25. Codes\12. Vedic RAG AI\Code Workspace\frontend_streamlit"
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note for WSL/Linux users**: If using ChromaDB, you may need:
   ```bash
   pip install pysqlite3-binary
   ```

## Running the Application

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

### Configuration
The app uses `.streamlit/config.toml` for theme and server settings. Modify this file to customize:
- Primary color
- Background colors
- Text color
- Font preferences
- Server settings

## Project Structure

```
frontend_streamlit/
├── main.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── .streamlit/
    └── config.toml                  # Streamlit configuration
```

## Architecture

### Key Components

**`initialize_vector_db()`**
- Placeholder for vector database initialization
- Returns connection status and indexed document count
- Implement with actual ChromaDB/Pinecone connection

**`get_rag_response(query, researcher_mode)`**
- Core RAG pipeline function
- Takes user query and researcher mode flag
- Returns response with sources and confidence scores
- Mock implementation provided; integrate with actual LLM backend

**`load_custom_css()`**
- Injects custom CSS for premium styling
- Handles dark theme, typography, and component styling
- Uses Google Fonts for Crimson Text and Inter

**`render_sidebar()`**
- Project information display
- Researcher Mode toggle
- Navigation menu
- Project metadata

**`render_chat_interface()`**
- Main chat display area
- Message history rendering
- Sources expander with confidence scores
- Input field with send button

**`render_sample_questions()`**
- Grid of pre-defined questions
- Click-to-query functionality

**`render_browse_scriptures()`**
- Scripture category browser
- Organized by text type (Vedas, Upanishads, etc.)

## Integration with Backend

To connect to your actual RAG backend:

1. **Update `get_rag_response()` function**:
   ```python
   def get_rag_response(query: str, researcher_mode: bool = False) -> Dict[str, Any]:
       # Replace mock implementation with actual API call
       response = requests.post(
           "http://localhost:8000/api/rag/query",
           json={"query": query, "researcher_mode": researcher_mode}
       )
       return response.json()
   ```

2. **Update `initialize_vector_db()` function**:
   ```python
   def initialize_vector_db():
       # Connect to actual ChromaDB or vector store
       client = chromadb.HttpClient(host="localhost", port=8000)
       return client
   ```

3. **Add API endpoint configuration**:
   - Create a `config.py` file with backend URL
   - Use environment variables for production

## Customization

### Changing Colors
Edit the CSS in `load_custom_css()`:
```python
primaryColor="#D4AF37"      # Gold accents
backgroundColor="#1a1a1a"   # Deep charcoal
secondaryBackgroundColor="#2d2d2d"  # Secondary dark
textColor="#F5F5F5"         # Off-white text
```

### Adding New Sample Questions
Modify the `sample_questions` list in `render_sample_questions()`:
```python
sample_questions = [
    "Your new question here",
    # ... more questions
]
```

### Modifying Scripture Categories
Update the `scripture_categories` dictionary in `render_browse_scriptures()`:
```python
scripture_categories = {
    "Your Category": ["Text 1", "Text 2", ...],
    # ... more categories
}
```

## Performance Optimization

- **Lazy Loading**: Sample questions and scripture categories load on demand
- **Session State**: Chat history persists within session using `st.session_state`
- **Caching**: Consider adding `@st.cache_data` for expensive operations
- **Streaming**: Implement token streaming for long responses

## Browser Compatibility

- Chrome/Chromium: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Edge: ✅ Full support

## Troubleshooting

### Port Already in Use
```bash
streamlit run main.py --server.port 8502
```

### CSS Not Loading
- Clear browser cache (Ctrl+Shift+Delete)
- Restart Streamlit server

### Slow Performance
- Check backend API response times
- Verify vector database is properly indexed
- Monitor system resources

## Future Enhancements

- [ ] Voice input for queries
- [ ] Export chat history as PDF
- [ ] Bookmark favorite sources
- [ ] Multi-language support
- [ ] Advanced filtering by scripture type
- [ ] Comparison view for multiple sources
- [ ] Integration with scholarly databases

## License

Part of the Digital Nalanda project. All rights reserved.

## Support

For issues or feature requests, contact the development team.
