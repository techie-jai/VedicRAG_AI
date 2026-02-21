# 🕉️ Ancient Vedic Wisdom AI: The RAG System

Welcome to the Vedic Wisdom AI project! This repository hosts the codebase for an advanced Retrieval-Augmented Generation (RAG) artificial intelligence system deeply rooted in ancient Indian knowledge, granthas, and epics.

The core aim of this system is to unlock the profound wisdom of ancient Vedic teachings for modern seekers. By conversing with this AI, users can discover timeless insights on leadership excellence, personal growth, spiritual enlightenment, and the art of living a meaningful life—all grounded entirely in the authentic verses of the original Sanskrit texts.

## 📖 The Vision

For thousands of years, the eternal truths of human potential, moral excellence, and spiritual awakening have been preserved in ancient Sanskrit literature. This project aims to make this transformative wisdom accessible to everyone.

Whether you are:

- **A leader** seeking wisdom for strategic excellence and ethical governance
- **An entrepreneur** building a meaningful legacy and positive impact
- **A student** pursuing knowledge, focus, and personal development
- **A seeker** exploring the deeper dimensions of consciousness and truth

This AI serves as your personal guide to the timeless teachings that have shaped civilizations and enlightened countless souls throughout history.

## 🗄️ The Dataset: Rooted in the Itihāsa Corpus

This system is built upon the magnificent Itihāsa dataset, a monumental corpus detailed in the 2021 research paper: "Itihāsa: A large-scale corpus for Sanskrit to English translation".

### Current Dataset Highlights:

- **85,895+ Translation Pairs**: A comprehensive collection of Sanskrit shlokas with precise English translations
- **The Ramayana**: 17,179 verses revealing the path of righteousness, courage, and ideal character through Lord Rama's journey
- **The Mahabharata**: 68,710 verses encompassing wisdom on duty, leadership, strategic excellence, and the ultimate purpose of life
- **Additional Scriptures**: Bhagavad Gita, Upanishads, and Vedas for holistic spiritual guidance

Note: Sanskrit's rich linguistic depth allows our RAG system to precisely match user queries with verses that capture the essence of their spiritual and personal aspirations.

## 🧠 How It Works (The RAG Architecture)

1. **Wisdom Ingestion**: Ancient Sanskrit verses and their English translations are carefully processed and organized for instant retrieval
2. **Intelligent Retrieval**: When you seek guidance (e.g., "What does the Bhagavad Gita teach about leadership?"), the system finds the most relevant teachings
3. **Enlightened Guidance**: The system presents authentic verses with context, helping you apply ancient wisdom to modern aspirations

## 🚀 Features

- **Authentic Wisdom**: Every insight is backed by original Sanskrit shlokas with accurate English translations
- **Practical Applications**: Ancient teachings adapted for modern leadership, personal growth, and ethical decision-making
- **Comprehensive Coverage**: Multiple Vedic sources including Ramayana, Mahabharata, Bhagavad Gita, Upanishads, and Vedas
- **Interactive Learning**: Command-line interface and ready-to-use text files for OpenUI and other RAG systems
- **Cultural Preservation**: Helping preserve and share India's invaluable spiritual heritage

## 🛠️ Getting Started

### Prerequisites

- Python 3.9+
- Internet connection for dataset download
- Optional: API keys for enhanced LLM integration

### Quick Setup

1. **Clone and Install:**
   ```bash
   git clone https://github.com/yourusername/vedic-wisdom-ai.git
   cd vedic-wisdom-ai
   pip install -r requirements.txt
   ```

2. **Generate the Wisdom Dataset:**
   ```bash
   python VedicDatasetGenerator.py
   ```
   This downloads and prepares 85,895+ verses from the greatest Vedic texts.

3. **Experience the Wisdom:**
   ```bash
   # Interactive wisdom exploration
   python simple_rag_demo.py

   # Test with sample queries
   python test_rag.py
   ```

## 📁 Dataset Structure

```
vedic_texts/
├── dataset_metadata.json          # Wisdom corpus statistics
├── vedic_corpus_part_1.txt        # First 20,000 verses of enlightenment
├── vedic_corpus_part_2.txt        # Next 20,000 verses of wisdom
├── vedic_corpus_part_3.txt        # Next 20,000 verses of guidance
├── vedic_corpus_part_4.txt        # Next 20,000 verses of insight
└── vedic_corpus_part_5.txt        # Final verses of transformation
```

### Dataset Summary:
- **Total Verses:** 85,895
- **Sources:** Itihasa (85,889), Bhagavad Gita (2), Upanishads (2), Vedas (2)
- **Categories:** Ramayana (17,179), Mahabharata (68,710), Bhagavad Gita (2), Upanishad (2), Veda (2)

## 🧠 Accessing Vedic Wisdom

### Interactive Mode:
```bash
python simple_rag_demo.py
```
Explore questions like:
- "Teach me about courageous leadership"
- "What does the Mahabharata say about wisdom?"
- "Guide me in the path of righteousness"
- "Share teachings on inner strength"

### OpenUI Integration:
The 5 text files in `vedic_texts/` are ready for OpenUI's RAG system. Each verse follows this enlightening format:
```
Source: Itihasa
Category: Ramayana
Title: Verse 1
Verse: 1
Sanskrit: [Original Sanskrit verse]
English: [Precise English translation]
---
```

### Programmatic Access:
```python
from simple_rag_demo import VedicRAGDemo

rag = VedicRAGDemo()
wisdom = rag.generate_response("leadership wisdom from Krishna")
print(wisdom)
```

## 📊 Wisdom Domains

The system illuminates these areas of human excellence:

- **🏆 Leadership Excellence**: Strategic wisdom from the Mahabharata's greatest kings and warriors
- **💪 Inner Strength**: Developing courage, resilience, and moral fortitude
- **🧘 Spiritual Growth**: Paths to enlightenment and self-realization
- **⚖️ Ethical Living**: The science of righteous conduct and Dharma
- **🌟 Personal Mastery**: Achieving excellence in character and conduct
- **🤝 Harmonious Relationships**: Building meaningful connections and social harmony

## 🗺️ Future Enlightenment

The foundation is strong, and future expansions will include:

- **📚 Expanded Scriptures**: Complete Upanishads, full Vedas, and comprehensive Puranas
- **🎯 Semantic Wisdom**: Advanced AI for deeper understanding of Vedic concepts
- **🌐 Global Interface**: Beautiful web interface for wisdom seekers worldwide
- **🎵 Sacred Sounds**: Audio guidance with proper Sanskrit pronunciation
- **📖 Scholarly Commentary**: Classical explanations by ancient Acharyas

## 🤝 Join the Wisdom Journey

We welcome contributions from wisdom seekers, developers, Sanskrit scholars, and spiritual enthusiasts!

### Areas for Contribution:

- **📖 Scripture Expansion**: Adding more Vedic texts and translations
- **🎯 Algorithm Enhancement**: Improving wisdom retrieval accuracy
- **💫 User Experience**: Creating more intuitive interfaces
- **📚 Educational Content**: Developing learning materials and guides
- **🔬 Research**: Exploring patterns in ancient wisdom traditions

### Contribution Path:
1. Fork this repository of enlightenment
2. Create your feature branch
3. Share your improvements with clear documentation
4. Submit a pull request to contribute to collective wisdom

## 📜 Gratitude and Acknowledgments

- **📄 Itihāsa Research**: Rahul Aralikatte, Miryam de Lhoneux, Anoop Kunchukuttan, and Anders Søgaard for their groundbreaking work in digitizing these sacred texts
- **🤖 Hugging Face**: For providing the technological foundation for wisdom preservation
- **🌍 Open Source Community**: For the collaborative spirit that makes such projects possible

## 📄 Sacred License

This project is open-source under the MIT License. The ancient Vedic texts belong to humanity's shared spiritual heritage and are freely shared for the benefit of all seekers.

## 🆘 Guidance and Support

For assistance on your wisdom journey:

1. Consult the troubleshooting section below
2. Ensure proper installation of all dependencies
3. Verify stable internet connection for dataset access
4. Create an issue on GitHub for personalized guidance

### Troubleshooting Wisdom:

**Challenge**: ModuleNotFoundError for 'datasets'
**Solution**: `pip install datasets huggingface_hub`

**Challenge**: Dataset download obstacles
**Solution**: Check connectivity and retry—the system includes resilience

**Challenge**: Large file memory concerns
**Solution**: Wisdom is already divided into manageable 20,000-verse segments

---

**🕉️ Begin your journey toward enlightenment today!**

*May this system illuminate your path with the eternal light of Vedic wisdom and guide you toward your highest potential.* 🙏

---

### Quick Enlightenment Commands:
```bash
# Prepare your environment
pip install -r requirements.txt

# Download sacred knowledge
python VedicDatasetGenerator.py

# Test the wisdom
python test_rag.py

# Begin your journey
python simple_rag_demo.py
```
