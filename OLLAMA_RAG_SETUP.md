# 🕉️ Vedic RAG with Ollama - Setup Guide

## Overview

This application combines **Vedic RAG (Retrieval-Augmented Generation)** with **Ollama** to create an interactive interface for exploring ancient Vedic wisdom using local AI models.

### Features

- **Local LLM Integration**: Uses Ollama for running models locally (no API keys needed)
- **Vedic RAG**: Retrieves relevant verses from Vedic texts as context
- **Beautiful UI**: Modern Streamlit interface with real-time responses
- **Conversation History**: Save and review past conversations
- **Flexible Model Selection**: Switch between different Ollama models

## Prerequisites

### 1. Install Ollama

Download and install Ollama from: https://ollama.ai

### 2. Pull a Model

Open terminal/command prompt and run:

```bash
ollama pull mistral
```

Or choose another model:
- `ollama pull neural-chat` (smaller, faster)
- `ollama pull llama2` (larger, more capable)
- `ollama pull dolphin-mixtral` (specialized)

### 3. Start Ollama Server

```bash
ollama serve
```

The server will run on `http://localhost:11434` by default.

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Vedic Dataset

Make sure you have the Vedic dataset. If not, run:

```bash
python VedicDatasetGenerator.py
```

This creates the `vedic_texts/` directory with the corpus.

## Running the Application

### Start the Streamlit App

```bash
streamlit run ollama_rag_ui.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

### 1. Configure Ollama Connection
- In the left sidebar, enter your Ollama server URL (default: `http://localhost:11434`)
- The app will show connection status
- Select an available model from the dropdown

### 2. Ask Questions
- Enter your question in the text input field
- Examples:
  - "What does the Bhagavad Gita say about duty?"
  - "How should I handle conflict according to Vedic wisdom?"
  - "What is the meaning of Dharma?"

### 3. View Results
- **Retrieved Verses**: See relevant Vedic verses with Sanskrit and English translations
- **Ollama Response**: Get an AI-generated answer that incorporates the verses
- **Save Conversation**: Optionally save the Q&A to `conversations.jsonl`

## Architecture

```
User Query
    ↓
RAG System (simple_rag_demo.py)
    ↓
Retrieve Relevant Verses
    ↓
Build Prompt with Context
    ↓
Ollama LLM
    ↓
Generate Response
    ↓
Display in UI
```

## Configuration Options

### RAG Settings
- **Max Verses to Retrieve**: Number of relevant verses to include (1-10)
- **Use RAG Context**: Toggle whether to include verses in the prompt

### Model Selection
- Switch models without restarting the app
- Each model has different speed/quality tradeoffs

## Troubleshooting

### "Cannot connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check the URL is correct (default: `http://localhost:11434`)
- On Windows, Ollama may run as a background service

### "No models found"
- Pull a model: `ollama pull mistral`
- List available models: `ollama list`

### "Request timeout"
- The model is slow to respond
- Try a smaller model like `neural-chat`
- Increase timeout or reduce max_verses

### "Dataset not found"
- Run `python VedicDatasetGenerator.py` to generate the dataset
- Ensure `vedic_texts/` directory exists in the workspace

## Performance Tips

1. **Use Smaller Models**: `neural-chat` is faster than `mistral`
2. **Reduce Verses**: Lower max_verses for faster retrieval
3. **Disable RAG**: For quick answers without context
4. **GPU Acceleration**: Ollama uses GPU if available (NVIDIA/Metal)

## File Structure

```
Code Workspace/
├── ollama_rag_ui.py           # Main Streamlit app
├── simple_rag_demo.py         # RAG system
├── requirements.txt           # Python dependencies
├── vedic_texts/               # Vedic dataset
│   ├── dataset_metadata.json
│   └── vedic_corpus_part_*.txt
├── conversations.jsonl        # Saved conversations (auto-created)
└── OLLAMA_RAG_SETUP.md       # This file
```

## Advanced Usage

### Custom Prompts

Edit the prompt in `ollama_rag_ui.py` (around line 180) to customize how Ollama generates responses.

### Batch Processing

For processing multiple queries:

```python
from ollama_rag_ui import query_ollama
from simple_rag_demo import VedicRAGDemo

rag = VedicRAGDemo()
queries = ["duty", "wisdom", "peace"]

for query in queries:
    verses = rag.search_verses(query, max_results=3)
    # Process verses...
```

### Integration with Other Tools

The RAG system can be integrated with:
- Discord bots
- Telegram bots
- Web APIs
- Desktop applications

## API Reference

### VedicRAGDemo

```python
from simple_rag_demo import VedicRAGDemo

rag = VedicRAGDemo()

# Search for verses
verses = rag.search_verses("duty", max_results=5)

# Generate response
response = rag.generate_response("What is dharma?", max_verses=3)
```

### Ollama Integration

```python
from ollama_rag_ui import query_ollama

response = query_ollama(
    model="mistral",
    prompt="Your prompt here",
    base_url="http://localhost:11434"
)
```

## Resources

- **Ollama**: https://ollama.ai
- **Streamlit**: https://streamlit.io
- **Vedic Texts**: Various Sanskrit sources in `vedic_texts/`

## License

This project combines open-source tools and Vedic texts for educational purposes.

## Support

For issues:
1. Check the Troubleshooting section
2. Verify Ollama is running
3. Check Python dependencies are installed
4. Review the console output for error messages
