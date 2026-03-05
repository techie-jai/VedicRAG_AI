🕉️ Ancient Vedic Wisdom AI: The RAG System

Welcome to the Vedic Wisdom AI project! This repository hosts the codebase for an advanced Retrieval-Augmented Generation (RAG) artificial intelligence system deeply rooted in ancient Indian knowledge, granthas, and epics.

The core aim of this system is to bridge the gap between profound ancient philosophy and modern-day challenges. By conversing with this AI, users can seek guidance through the lowest and toughest points in their lives, find strategic insights on leadership and "building an empire," or simply explore the ethical and spiritual tenets of Dharma—all grounded entirely in the authentic verses of the original texts.

📖 The Vision

For thousands of years, the answers to the complexities of human life, morality, conflict, and governance have been preserved in ancient Sanskrit literature. This project aims to democratize that knowledge.

Whether you are:

- A student seeking clarity and focus
- A leader or entrepreneur looking for strategic wisdom (akin to the strategic diplomacy of the Mahabharata)
- An individual navigating personal grief or moral dilemmas

This AI acts as a philosophical companion, querying thousands of ancient verses to provide contextual, translated, and highly relevant guidance.

🗄️ The Dataset: Rooted in the Itihāsa Corpus

This system is initially trained and embedded using the Itihāsa dataset, a monumental corpus detailed in the 2021 research paper: "Itihāsa: A large-scale corpus for Sanskrit to English translation".

**Current Dataset Highlights:**

- **93,000+ Translation Pairs**: A massive collection of Sanskrit shlokas mapped to their English translations
- **The Ramayana**: Contains over 19,000 translation pairs extracted from 642 chapters, focusing on the life, ethics, and ideals of Lord Rama
- **The Mahabharata**: Contains over 73,000 translation pairs extracted from 2,110 chapters, encompassing complex politics, war, duty, and the ultimate teachings of life

Note: As noted in the foundational research, Sanskrit is highly agglutinative and morphologically rich. By leveraging this rigorously aligned dataset, our RAG system can accurately retrieve the exact shlokas that match the semantic intent of a user's English query.

🧠 How It Works (The RAG Architecture)

1. **Knowledge Ingestion**: The English translations and their corresponding Sanskrit shlokas from the dataset are embedded using advanced dense vector models and stored in a Vector Database
2. **Contextual Retrieval**: When a user asks a question (e.g., "How do I find courage when I have lost everything?"), the system searches the vector database for the most semantically relevant teachings from the epics
3. **Augmented Generation**: A Large Language Model (LLM) synthesizes the retrieved shlokas, interprets their philosophical meaning in the context of the user's query, and outputs a personalized, guiding response that cites the original verses

🚀 Features

- **Authentic Citations**: Every piece of advice provided by the AI is backed by a specific quoted shloka (in Sanskrit/Devanagari) along with its English translation
- **Context-Aware Guidance**: Capable of mapping abstract ancient concepts (like Karma, Dharma, and Niti) to modern psychological and strategic scenarios
- **Interactive UI**: A conversational interface designed for deep, reflective, and continuous dialogue

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- API keys for your preferred LLM (e.g., OpenAI, Anthropic, or local models like Llama 3) - optional for basic demo
- Vector Database instance (e.g., Pinecone, Milvus, or local ChromaDB) - optional for basic demo

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/vedic-wisdom-ai.git
   cd vedic-wisdom-ai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate the Vedic Dataset:**
   ```bash
   python VedicDatasetGenerator.py
   ```
   This will download and process:
   - **85,889 verses** from the Itihāsa dataset (Ramayana & Mahabharata)
   - **Bhagavad Gita** verses
   - **Upanishad** selections
   - **Vedic** hymns and verses

   The dataset will be saved in the `vedic_texts/` directory as 5 manageable text files.

4. **Run the RAG Demo:**
   ```bash
   # Interactive demo
   python simple_rag_demo.py
   
   # Or test with predefined queries
   python test_rag.py
   ```

### 📁 Dataset Structure

After running the dataset generator, you'll have:

```
vedic_texts/
├── dataset_metadata.json          # Dataset statistics and info
├── vedic_corpus_part_1.txt        # First 20,000 verses
├── vedic_corpus_part_2.txt        # Next 20,000 verses
├── vedic_corpus_part_3.txt        # Next 20,000 verses
├── vedic_corpus_part_4.txt        # Next 20,000 verses
└── vedic_corpus_part_5.txt        # Remaining verses
```

**Dataset Summary:**
- **Total Verses:** 85,895
- **Sources:** Itihasa (85,889), Bhagavad Gita (2), Upanishads (2), Vedas (2)
- **Categories:** Ramayana (17,179), Mahabharata (68,710), Bhagavad Gita (2), Upanishad (2), Veda (2)

### 🧠 How the RAG System Works

1. **Data Ingestion:** The verses are loaded from the text files into memory
2. **Query Processing:** User queries are analyzed for keywords and semantic meaning
3. **Retrieval:** Relevant verses are found using keyword matching and scoring
4. **Response Generation:** The system presents the most relevant verses with context

### 🚀 Advanced Features

For production use, you can enhance the system with:

- **Vector Embeddings**: Use sentence-transformers for semantic search
- **Vector Database**: Store embeddings in ChromaDB, Pinecone, or Milvus
- **LLM Integration**: Connect to OpenAI, Anthropic, or local models for enhanced responses
- **Web Interface**: Use Streamlit or Flask for a user-friendly UI

### 🔧 Environment Setup (Optional)

For advanced features with LLM integration, create a `.env` file:

```bash
LLM_API_KEY=your_api_key_here
VECTOR_DB_URL=your_db_url_here
```

## 🗺️ Future Roadmap

While the foundation is built on the Ramayana and Mahabharata, the corpus of Vedic literature is vast. Future updates to the vector database will include:

- **The Upanishads**: For deep metaphysical and spiritual queries
- **The Vedas** (Rig, Yajur, Sama, Atharva): For foundational ancient knowledge
- **Puranas & Neeti Shastras** (e.g., Chanakya Niti): For highly practical, unvarnished advice on statecraft, economics, and human behavior
- **Bhagavad Gita** (Standalone Deep-Dive): Enhanced multi-layered commentary retrieval

## 🤝 Contributing

We welcome contributions from developers, Sanskrit scholars, and history enthusiasts! Whether it's refining the RAG retrieval accuracy, adding new texts to the vector database, or improving the frontend, please feel free to open a Pull Request.

## 📜 Acknowledgements

Thanks to the authors of the Itihāsa research paper (Rahul Aralikatte, Miryam de Lhoneux, Anoop Kunchukuttan, Anders Søgaard) for their incredible work in digitizing and aligning these ancient texts.

---

**🕉️ Start your journey into ancient wisdom today!**
