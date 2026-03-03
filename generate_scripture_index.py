import os
import json
from pathlib import Path
from collections import defaultdict

def get_file_size(filepath):
    """Get file size in KB"""
    try:
        size_bytes = os.path.getsize(filepath)
        return f"{size_bytes / 1024:.1f} KB"
    except:
        return "N/A"

def scan_dharmaganj():
    """Scan dharmaganj folder and collect all scripture information"""
    
    dharmaganj_path = "dharmaganj"
    scriptures = defaultdict(lambda: defaultdict(list))
    
    # Walk through all directories
    for root, dirs, files in os.walk(dharmaganj_path):
        for file in files:
            if file.endswith(('.txt', '.xml', '.json')) and file != 'master_catalog.json':
                filepath = os.path.join(root, file)
                rel_path = filepath.replace('\\', '/')
                
                # Parse the path to extract building, domain, and file info
                parts = rel_path.split('/')
                
                if len(parts) >= 3:
                    building = parts[1]  # ratnodadhi, ratnasagara, ratnaranjaka, bagdevibhandar
                    domain = parts[2] if len(parts) > 2 else "unknown"
                    
                    # Determine language and format
                    file_ext = os.path.splitext(file)[1]
                    if file_ext == '.xml':
                        file_format = "XML"
                        language = "Sanskrit"
                    elif file_ext == '.txt':
                        file_format = "TXT"
                        language = "Sanskrit"
                    elif file_ext == '.json':
                        file_format = "JSON"
                        language = "Sanskrit"
                    else:
                        file_format = file_ext.upper()
                        language = "Unknown"
                    
                    file_size = get_file_size(filepath)
                    
                    scripture_info = {
                        "filename": file,
                        "path": rel_path,
                        "building": building,
                        "domain": domain,
                        "format": file_format,
                        "language": language,
                        "size": file_size
                    }
                    
                    scriptures[building][domain].append(scripture_info)
    
    return scriptures

def load_master_catalog():
    """Load the master catalog JSON"""
    try:
        with open('dharmaganj/bagdevibhandar/master_catalog.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def get_scripture_description(filename, domain):
    """Get description for a scripture based on filename and domain"""
    descriptions = {
        # Vedas
        "vedic_corpus": "Vedic texts - Rig, Sama, Yajur, Atharva Vedas with hymns and rituals",
        "Rig Veda": "Oldest Veda with 1,028 hymns praising deities and describing cosmology",
        "Sama Veda": "Veda of Melodies - hymns arranged for liturgical chanting",
        "Yajur Veda": "Veda of Sacrifices - detailed instructions for Vedic rituals",
        "Atharva Veda": "Veda of Incantations - spells, charms, and metaphysical teachings",
        
        # Upanishads
        "upanishad": "Philosophical treatises on Brahman and Atman",
        "Upanishads": "Foundation of Vedantic philosophy exploring ultimate reality",
        
        # Bhagavad Gita
        "Bhagavad Gita": "Sacred dialogue between Krishna and Arjuna on dharma and liberation",
        "srimadbhagavadgita": "Bhagavad Gita - teachings on duty, devotion, and paths to liberation",
        
        # Puranas
        "purana": "Mythological narratives on cosmology and divine principles",
        "Puranas": "Post-Vedic texts with mythology, cosmology, and spiritual teachings",
        
        # Epics
        "itihasa": "Great Epics - Ramayana and Mahabharata with philosophical teachings",
        "Mahabharata": "World's longest epic on the Kurukshetra war and human nature",
        "Ramayana": "Epic tale of Prince Rama's exile teaching dharma and righteousness",
        
        # Medicine (Ayurveda)
        "cikitsavidya": "Ayurvedic medical treatises on healing and herbal remedies",
        "carakasamhita": "Charaka Samhita - foundational Ayurvedic medical text",
        "susrutasamhita": "Sushruta Samhita - surgical treatises and medical procedures",
        "astangahrdayasamhita": "Ashtanga Hridaya - comprehensive Ayurvedic medicine guide",
        
        # Logic & Epistemology
        "nyaya_pramana": "Logical treatises on epistemology and valid knowledge",
        "nyayamanjari": "Compendium of Nyaya logic and philosophical reasoning",
        "pramanavarttika": "Buddhist epistemology and theory of valid knowledge",
        
        # Grammar
        "vyakarana": "Sanskrit grammar and linguistic analysis",
        "bhartrhari-vakyapadiya": "Philosophy of language and sentence meaning",
        
        # Political Science
        "arthashastra": "Kautilya's treatise on statecraft and political economy",
        "kautalyarthasastra": "Ancient text on governance, economics, and diplomacy",
        
        # Classical Poetry & Drama
        "kavya": "Classical Sanskrit poetry and dramatic literature",
        "bana-kadambari": "Romantic narrative prose by Bana",
        "asvaghosa-buddhacarita": "Life of Buddha in poetic form",
        
        # Sutras & Philosophical Works
        "sutra": "Aphoristic philosophical texts and commentaries",
        "patanjalayogasastra": "Yoga Sutras - foundational text on Raja Yoga",
        "astavakragita": "Philosophical teachings on non-dualism",
        
        # Modern & Contemporary
        "vividha": "Miscellaneous texts including modern and contemporary works",
    }
    
    # Check various keys for description
    for key, desc in descriptions.items():
        if key.lower() in filename.lower() or key.lower() in domain.lower():
            return desc
    
    return f"Text from {domain} domain"

def generate_markdown_index(scriptures, catalog):
    """Generate comprehensive markdown index"""
    
    markdown = """# 📚 Complete Scripture & Text Index - Dharmaganj Digital Repository

**Last Updated**: March 2026  
**Total Texts**: 183+ manuscripts and text files  
**Format**: Comprehensive catalog with metadata for all books and scriptures

---

## 📋 Index Overview

This index contains detailed information about every book, scripture, and text in the Dharmaganj repository, organized by:
- **Building**: Ratnodadhi (Sacred), Ratnasagara (Technical), Ratnaranjaka (Narrative)
- **Domain**: Subject classification (Vedas, Medicine, Logic, Poetry, etc.)
- **Language**: Original language and script
- **Format**: File format (TXT, XML, JSON)
- **Size**: File size for reference

---

"""
    
    # Building descriptions
    building_info = {
        "ratnodadhi": {
            "title": "🏛️ Ratnodadhi (The Sea of Jewels)",
            "description": "Core/Sacred foundational texts - philosophical and spiritual knowledge",
            "emoji": "✨"
        },
        "ratnasagara": {
            "title": "🏛️ Ratnasagara (The Ocean of Jewels)",
            "description": "Technical/Scientific knowledge - medical, logical, and scholarly treatises",
            "emoji": "🔬"
        },
        "ratnaranjaka": {
            "title": "🏛️ Ratnaranjaka (The Jewel-Adorned)",
            "description": "Narrative/Cultural heritage - epics, poetry, and literature",
            "emoji": "📖"
        },
        "bagdevibhandar": {
            "title": "🏛️ Bagdevibhandar (The Master Index)",
            "description": "Central metadata authority and reference materials",
            "emoji": "📑"
        }
    }
    
    # Generate content for each building
    for building in ["ratnodadhi", "ratnasagara", "ratnaranjaka", "bagdevibhandar"]:
        if building not in scriptures and building != "bagdevibhandar":
            continue
        
        info = building_info.get(building, {})
        markdown += f"\n## {info.get('title', building)}\n"
        markdown += f"**{info.get('description', '')}**\n\n"
        
        if building == "bagdevibhandar":
            # Special handling for bagdevibhandar
            markdown += "| Filename | Domain | Format | Language | Size |\n"
            markdown += "|----------|--------|--------|----------|------|\n"
            
            for root, dirs, files in os.walk("dharmaganj/bagdevibhandar"):
                for file in files:
                    if file.endswith(('.json', '.pdf')):
                        filepath = os.path.join(root, file)
                        rel_path = filepath.replace('\\', '/')
                        domain = os.path.basename(os.path.dirname(filepath))
                        file_ext = os.path.splitext(file)[1]
                        size = get_file_size(filepath)
                        
                        markdown += f"| {file} | {domain} | {file_ext.upper()} | Reference | {size} |\n"
        else:
            # Regular buildings
            if building in scriptures:
                for domain in sorted(scriptures[building].keys()):
                    texts = scriptures[building][domain]
                    
                    markdown += f"\n### {domain.replace('_', ' ').title()} ({len(texts)} texts)\n"
                    markdown += f"**Description**: {get_scripture_description('', domain)}\n\n"
                    
                    markdown += "| Scripture/Text | Filename | Format | Language | Size | Path |\n"
                    markdown += "|---|---|---|---|---|---|\n"
                    
                    for text in sorted(texts, key=lambda x: x['filename']):
                        # Get human-readable name
                        display_name = text['filename'].replace('_', ' ').replace('.txt', '').replace('.xml', '').replace('.json', '')
                        desc = get_scripture_description(text['filename'], domain)
                        
                        markdown += f"| {desc} | `{text['filename']}` | {text['format']} | {text['language']} | {text['size']} | `{text['path']}` |\n"
                    
                    markdown += "\n"
    
    return markdown

def main():
    print("Scanning dharmaganj folder...")
    scriptures = scan_dharmaganj()
    
    print("Loading master catalog...")
    catalog = load_master_catalog()
    
    print("Generating markdown index...")
    markdown_content = generate_markdown_index(scriptures, catalog)
    
    # Save to file
    output_file = "SCRIPTURE_INDEX.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"\n✅ Index generated successfully!")
    print(f"📄 Output file: {output_file}")
    
    # Print summary statistics
    total_texts = sum(len(texts) for domain_texts in scriptures.values() for texts in domain_texts.values())
    print(f"\n📊 Summary Statistics:")
    print(f"   Total texts indexed: {total_texts}")
    
    for building in ["ratnodadhi", "ratnasagara", "ratnaranjaka"]:
        if building in scriptures:
            count = sum(len(texts) for texts in scriptures[building].values())
            print(f"   {building}: {count} texts")

if __name__ == "__main__":
    main()
