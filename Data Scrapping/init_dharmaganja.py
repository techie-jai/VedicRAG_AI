import os
import json

def initialize_dharmaganj():
    """
    Initializes the Dharmaganj RAG directory structure inspired by Nalanda University.
    """
    root = "dharmaganj"
    
    # Tier 1 & 2 Structure Definition
    hierarchy = {
        "bagdevibhandar": {
            "description": "The Global Index (Metadata & Lookups)",
            "subdirs": ["schema_definitions"]
        },
        "ratnodadhi": {
            "description": "BUILDING 1: THE CORE (Sacred & Foundational)",
            "subdirs": ["shruti", "upanishads", "mahayana_sutras"]
        },
        "ratnasagara": {
            "description": "BUILDING 2: THE OCEAN (Technical & Academic)",
            "subdirs": ["vyakarana", "nyaya_pramana", "cikitsavidya", "jyotisha", "arthashastra"]
        },
        "ratnaranjaka": {
            "description": "BUILDING 3: THE ADORNED (Cultural & Literary)",
            "subdirs": ["itihasa", "purana", "kavya", "vividha"]
        }
    }

    # Data lifecycle sub-folders for Tier 2
    lifecycle_dirs = ["raw", "clean", "embedded"]

    print(f"Initializing {root} architecture...")

    # Create Root
    os.makedirs(root, exist_ok=True)

    for building, config in hierarchy.items():
        building_path = os.path.join(root, building)
        os.makedirs(building_path, exist_ok=True)
        print(f"  [Building] Created {building_path}")

        for subject in config["subdirs"]:
            subject_path = os.path.join(building_path, subject)
            os.makedirs(subject_path, exist_ok=True)
            
            # Special handling for bagdevibhandar which doesn't follow the 3-tier lifecycle exactly as per request
            if building != "bagdevibhandar":
                for lifecycle in lifecycle_dirs:
                    path = os.path.join(subject_path, lifecycle)
                    os.makedirs(path, exist_ok=True)
            
        # Create initial files for bagdevibhandar
        if building == "bagdevibhandar":
            master_catalog_path = os.path.join(building_path, "master_catalog.json")
            if not os.path.exists(master_catalog_path):
                with open(master_catalog_path, 'w') as f:
                    json.dump({"version": "1.0", "buildings": list(hierarchy.keys()), "catalog": []}, f, indent=4)
                print(f"    [File] Created {master_catalog_path}")

    # Generate README.md
    readme_content = f"""# Dharmaganj: The Nalanda-Inspired RAG Architecture

This directory structure is modeled after the **Dharmaganj** (Mart of Religion), the legendary library of ancient Nalanda University. The three main buildings reflect the organizational wisdom of one of the world's first great academic institutions.

## The Hierarchy

### 1. Bagdevibhandar (The Global Index)
*   **Purpose**: Metadata, schemas, and master lookups.
*   **Contents**: `master_catalog.json` and schema definitions for Lipi (script), Shakha (recension), and Bhashya (commentaries).

### 2. Ratnodadhi (The Ocean of Gems) - Building 1
*   **Significance**: Historically a nine-story building housing the most sacred and foundational texts.
*   **Subjects**: 
    *   `shruti`: Vedas (Rig, Sama, Yajur, Atharva).
    *   `upanishads`: The 108 core Upanishads.
    *   `mahayana_sutras`: Core Buddhist Sutras like Prajnaparamita.

### 3. Ratnasagara (The Sea of Gems) - Building 2
*   **Significance**: Dedicated to technical treatises, sciences, and academic disciplines.
*   **Subjects**:
    *   `vyakarana`: Grammar and Linguistics (Panini, Patanjali).
    *   `nyaya_pramana`: Logic and Epistemology (Dignaga, Dharmakirti).
    *   `cikitsavidya`: Medicine and Ayurveda (Charaka, Sushruta).
    *   `jyotisha`: Astronomy and Mathematics (Aryabhata).
    *   `arthashastra`: Statecraft and Political Economy (Kautilya).

### 4. Ratnaranjaka (The Adorned with Gems) - Building 3
*   **Significance**: For cultural, literary, and general knowledge.
*   **Subjects**:
    *   `itihasa`: Epics like Ramayana and Mahabharata.
    *   `purana`: The 18 Mahapuranas.
    *   `kavya`: Classical Poetry and Drama (Kalidasa).
    *   `vividha`: Miscellaneous secular humanities.

## Data Lifecycle Pattern
Each subject folder contains three distinct stages:
*   `raw/`: Original source files (JSON, XML, CSV, TXT).
*   `clean/`: Pre-processed, sandhi-split, or lemmatized text ready for tokenization.
*   `embedded/`: Vector index exports and embeddings for the RAG system.
"""
    
    with open(os.path.join(root, "README.md"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  [Doc] Created {os.path.join(root, 'README.md')}")

    print("\nArchitecture initialization complete. The Dharmaganj is ready for ingestion.")

if __name__ == "__main__":
    initialize_dharmaganj()
