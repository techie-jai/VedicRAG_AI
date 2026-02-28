# Dharmaganj Digital Repository: Organizational Architecture

## 1. Introduction
This repository is a digital reconstruction of the **Dharmaganj** ("Treasury of Truth"), the legendary library complex of ancient Nalanda University. Our goal is to build a high-performance Retrieval-Augmented Generation (RAG) system by mimicking the sophisticated information architecture used by ancient scholars to manage millions of manuscripts.

For a modern RAG system, this structure allows for **Agentic Semantic Routing**. Instead of performing a brute-force search across a single massive index, our agents route queries to specific "Buildings" or "Niches" based on the domain of knowledge required.

## 2. The Philosophy of Three Buildings
Following the historical accounts of pilgrims like Xuanzang and Yijing, the data is partitioned into three primary architectural nodes (Tier 1 directories).

### 🏛️ Ratnodadhi (The Sea of Jewels)
**The Science**: Historically a nine-story skyscraper, this building housed the "Core/Sacred" knowledge.

**Logic**: This directory stores foundational philosophical and spiritual texts that provide the "ground truth" for the entire system.

**What goes here**:
*   **Shruti**: The four Vedas (Rig, Sama, Yajur, Atharva) and their Samhitas.
*   **Upanishads**: The Mukhya and minor Upanishads.
*   **Core Sutras**: Foundational Mahayana texts like the Prajnaparamita and Guhyasamaja.

### 🏛️ Ratnasagara (The Ocean of Jewels)
**The Science**: The largest building, specializing in technical treatises (Shastras) and rare scientific works.

**Logic**: This is the "Expert/Academic" node. It stores logical, medical, and scientific data that requires high precision and specific domain expertise.

**What goes here**:
*   **Cikitsavidya (Medicine)**: Ayurveda (Charaka, Sushruta Samhitas).
*   **Nyaya-Pramana (Logic)**: Works on logic and epistemology by masters like Dignaga and Dharmakirti.
*   **Vyakarana (Grammar)**: Mathematical linguistics like Panini’s Astadhyayi.
*   **Jyotisha (Astronomy)**: Treatises by Aryabhata and others.
*   **Arthashastra**: Technical manuals on statecraft and economy.

### 🏛️ Ratnaranjaka (The Jewel-Adorned)
**The Science**: Focused on the humanities, literature, and general cultural knowledge.

**Logic**: This is the "Narrative/Cultural" node, ideal for queries regarding history, ethics, and artistic traditions.

**What goes here**:
*   **Itihasa**: The Great Epics (Ramayana, Mahabharata).
*   **Purana**: The 18 Mahapuranas.
*   **Kavya**: Classical poetry and drama (e.g., Kalidasa).
*   **Vividha**: Secular literature, music, and the arts.

## 3. Data Storage & Lifecycle (The "Niche" System)
In Nalanda, manuscripts were stored in stone niches (Alcoves) to prevent decay. In our system, every subject folder follows a standardized three-stage lifecycle:

*   **`/raw`**: The original, immutable files (JSON, XML, CSV). This preserves the "Scribal Integrity" of the source.
*   **`/clean`**: Data that has been normalized, with Sandhi-splitting and lemmatization applied for machine-readability.
*   **`/embedded`**: The final vector representations (e.g., FAISS or ChromaDB exports) ready for the RAG retriever.

## 4. Bagdevibhandar: The Global Master Index
The `bagdevibhandar` directory acts as our central metadata authority, mirroring the historical palm-leaf catalog system.

Every ingestion must include a metadata entry with the following Nalanda-standard fields:
*   `nalanda_building`: (Ratnodadhi | Ratnasagara | Ratnaranjaka)
*   `subject_domain`: (e.g., Ayurveda, Vyakarana, Shruti)
*   `lipi`: The original script (e.g., Devanagari, Grantha, Sharada).
*   `shakha/recension`: The specific tradition or lineage of the text.
*   `bhashya`: Links to associated commentaries (e.g., Shankara's Bhashyas).

## 5. Contributor Guide
When placing new data, ask:
1. "Is this foundational wisdom?" ➡️ **Ratnodadhi**
2. "Is this technical or logical?" ➡️ **Ratnasagara**
3. "Is this narrative or artistic?" ➡️ **Ratnaranjaka**

By adhering to this structure, we ensure that our RAG system doesn't just "search text," but navigates the "Sea of Jewels" with the same scientific precision as the masters of Nalanda.

## 6. Current Repository Status
The repository is currently seeded with foundational and narrative data:

| Building | Subject | Data Source | Files | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Ratnodadhi** | `shruti` | Vedic Corpus, Bhagavad Gita | 5 (`raw/`) | Initialized |
| **Ratnaranjaka** | `itihasa` | Ramayana, Mahabharata | 5 (`raw/`) | Initialized |
| **Ratnasagara** | Technical | Ayurveda, Nyaya, etc. | 0 | Awaiting Ingestion |
| **Bagdevibhandar** | Metadata | Master Catalog, Schemas | 3 | Active |

All data is indexed in `bagdevibhandar/master_catalog.json` with appropriate metadata fields (Lipi, Shakha, Domain).
