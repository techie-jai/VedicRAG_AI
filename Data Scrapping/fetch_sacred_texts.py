import cloudscraper
import os
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# Base URL for sacred-texts Hindu collection
BASE_URL = "https://www.sacred-texts.com/hin"
OUTPUT_DIR = "sacred_texts_hindu"

# Dictionary of text titles and their URLs
HINDU_TEXTS = {
    # The Vedas
    "Rig Veda": {
        "url": "https://www.sacred-texts.com/hin/rigveda.htm",
        "category": "Vedas"
    },
    "Rig-Veda (Sanskrit)": {
        "url": "https://www.sacred-texts.com/hin/rvsan/index.htm",
        "category": "Vedas"
    },
    "Vedic Hymns Part I (SBE 32)": {
        "url": "https://www.sacred-texts.com/hin/sbe32/index.htm",
        "category": "Vedas"
    },
    "Vedic Hymns Part II (SBE 46)": {
        "url": "https://www.sacred-texts.com/hin/sbe46/index.htm",
        "category": "Vedas"
    },
    "A Vedic Reader for Students": {
        "url": "https://www.sacred-texts.com/hin/vedaread.htm",
        "category": "Vedas"
    },
    "The Sama-Veda": {
        "url": "https://www.sacred-texts.com/hin/sv.htm",
        "category": "Vedas"
    },
    "The Yajur Veda (Taittiriya Sanhita)": {
        "url": "https://www.sacred-texts.com/hin/yv.htm",
        "category": "Vedas"
    },
    "The Texts of the White Yajurveda": {
        "url": "https://www.sacred-texts.com/hin/wyv/index.htm",
        "category": "Vedas"
    },
    "The Hymns of the Atharvaveda": {
        "url": "https://www.sacred-texts.com/hin/av/index.htm",
        "category": "Vedas"
    },
    "The Atharva-Veda (SBE 42)": {
        "url": "https://www.sacred-texts.com/hin/sbe42/index.htm",
        "category": "Vedas"
    },
    
    # Upanishads
    "The Upanishads": {
        "url": "https://www.sacred-texts.com/hin/upan/index.htm",
        "category": "Upanishads"
    },
    "The Upanishads Part I (SBE 1)": {
        "url": "https://www.sacred-texts.com/hin/sbe01/index.htm",
        "category": "Upanishads"
    },
    "The Upanishads Part II (SBE 15)": {
        "url": "https://www.sacred-texts.com/hin/sbe15/index.htm",
        "category": "Upanishads"
    },
    "Thirty Minor Upanishads": {
        "url": "https://www.sacred-texts.com/hin/tmu/index.htm",
        "category": "Upanishads"
    },
    "From the Upanishads": {
        "url": "https://www.sacred-texts.com/hin/ftu/index.htm",
        "category": "Upanishads"
    },
    
    # Puranas
    "The Vishnu Purana": {
        "url": "https://www.sacred-texts.com/hin/vp/index.htm",
        "category": "Puranas"
    },
    "The Garuda Purana": {
        "url": "https://www.sacred-texts.com/hin/gpu/index.htm",
        "category": "Puranas"
    },
    "The S'rimad Devî Bhâgawatam": {
        "url": "https://www.sacred-texts.com/hin/db/index.htm",
        "category": "Puranas"
    },
    "The Devî Gita": {
        "url": "https://www.sacred-texts.com/hin/dg/index.htm",
        "category": "Puranas"
    },
    "The Prem Sagur (Prem Sagar)": {
        "url": "https://www.sacred-texts.com/hin/ps/index.htm",
        "category": "Puranas"
    },
    "Kundalini: The Mother of the Universe": {
        "url": "https://www.sacred-texts.com/hin/kmu/index.htm",
        "category": "Puranas"
    },
    
    # Other Primary Texts
    "The Laws of Manu": {
        "url": "https://www.sacred-texts.com/hin/manu.htm",
        "category": "Primary Texts"
    },
    "The Sacred Laws of the Âryas Part I (SBE 2)": {
        "url": "https://www.sacred-texts.com/hin/sbe02/index.htm",
        "category": "Primary Texts"
    },
    "The Sacred Laws of the Âryas Part II (SBE 14)": {
        "url": "https://www.sacred-texts.com/hin/sbe14/index.htm",
        "category": "Primary Texts"
    },
    "The Institutes of Vishnu (SBE 7)": {
        "url": "https://www.sacred-texts.com/hin/sbe07/index.htm",
        "category": "Primary Texts"
    },
    "The Minor Law Books (SBE 33)": {
        "url": "https://www.sacred-texts.com/hin/sbe33/index.htm",
        "category": "Primary Texts"
    },
    "Satapatha Brahmana Part I (SBE 12)": {
        "url": "https://www.sacred-texts.com/hin/sbr/sbe12/index.htm",
        "category": "Primary Texts"
    },
    "Satapatha Brahmana Part II (SBE 26)": {
        "url": "https://www.sacred-texts.com/hin/sbr/sbe26/index.htm",
        "category": "Primary Texts"
    },
    "Satapatha Brahmana Part III (SBE 41)": {
        "url": "https://www.sacred-texts.com/hin/sbr/sbe41/index.htm",
        "category": "Primary Texts"
    },
    "Satapatha Brahmana Part IV (SBE 43)": {
        "url": "https://www.sacred-texts.com/hin/sbr/sbe43/index.htm",
        "category": "Primary Texts"
    },
    "Satapatha Brahmana Part V (SBE 44)": {
        "url": "https://www.sacred-texts.com/hin/sbr/sbe44/index.htm",
        "category": "Primary Texts"
    },
    "The Grihya Sutras Part 1 (SBE 29)": {
        "url": "https://www.sacred-texts.com/hin/sbe29/index.htm",
        "category": "Primary Texts"
    },
    "The Grihya Sutras Part 2 (SBE 30)": {
        "url": "https://www.sacred-texts.com/hin/sbe30/index.htm",
        "category": "Primary Texts"
    },
    
    # The Epics
    "The Mahabharata": {
        "url": "https://www.sacred-texts.com/hin/maha/index.htm",
        "category": "Epics"
    },
    "The Mahabharata in Sanskrit": {
        "url": "https://www.sacred-texts.com/hin/mbs/index.htm",
        "category": "Epics"
    },
    "Rámáyan Of Válmíki": {
        "url": "https://www.sacred-texts.com/hin/rama/index.htm",
        "category": "Epics"
    },
    "The Ramayana in Sanskrit": {
        "url": "https://www.sacred-texts.com/hin/rys/index.htm",
        "category": "Epics"
    },
    "The Ramayana and Mahabharata (Abridged)": {
        "url": "https://www.sacred-texts.com/hin/dutt/index.htm",
        "category": "Epics"
    },
    "Indian Idylls": {
        "url": "https://www.sacred-texts.com/hin/ii.htm",
        "category": "Epics"
    },
    "Love and Death": {
        "url": "https://www.sacred-texts.com/hin/lad/index.htm",
        "category": "Epics"
    },
    
    # Bhagavad Gita
    "The Bhagavadgîtâ (SBE 8)": {
        "url": "https://www.sacred-texts.com/hin/sbe08/index.htm",
        "category": "Bhagavad Gita"
    },
    "The Bhagavad Gita in Sanskrit": {
        "url": "https://www.sacred-texts.com/hin/bgs/index.htm",
        "category": "Bhagavad Gita"
    },
    "Srimad-Bhagavad-Gita": {
        "url": "https://www.sacred-texts.com/hin/sbg/index.htm",
        "category": "Bhagavad Gita"
    },
    "The Bhagavad Gita (International Gita Society)": {
        "url": "https://www.sacred-texts.com/hin/gita/agsgita.htm",
        "category": "Bhagavad Gita"
    },
    "The Bhagavad Gita (Edwin Arnold)": {
        "url": "https://www.sacred-texts.com/hin/gita/index.htm",
        "category": "Bhagavad Gita"
    },
    
    # Vedanta
    "The Vedântâ-Sûtras with Râmânuja commentary (SBE 48)": {
        "url": "https://www.sacred-texts.com/hin/sbe48/index.htm",
        "category": "Vedanta"
    },
    "The Vedântâ-Sûtras Part I with Sankarâkârya commentary (SBE 34)": {
        "url": "https://www.sacred-texts.com/hin/sbe34/index.htm",
        "category": "Vedanta"
    },
    "The Vedântâ-Sûtras Part II with Sankarâkârya commentary (SBE 38)": {
        "url": "https://www.sacred-texts.com/hin/sbe38/index.htm",
        "category": "Vedanta"
    },
    "The Crest-Jewel of Wisdom": {
        "url": "https://www.sacred-texts.com/hin/cjw/index.htm",
        "category": "Vedanta"
    },
    "Brahma-Knowledge": {
        "url": "https://www.sacred-texts.com/hin/bk/index.htm",
        "category": "Vedanta"
    },
    "Select Works of Sri Sankaracharya": {
        "url": "https://www.sacred-texts.com/hin/wos/index.htm",
        "category": "Vedanta"
    },
    
    # Later Texts
    "The Yoga Sutras of Patanjali (Johnston)": {
        "url": "https://www.sacred-texts.com/hin/yogasutra.htm",
        "category": "Later Texts"
    },
    "The Yoga Sutras of Patanjali (Alternative)": {
        "url": "https://www.sacred-texts.com/hin/ysp/index.htm",
        "category": "Later Texts"
    },
    "The Hatha Yoga Pradipika": {
        "url": "https://www.sacred-texts.com/hin/hyp/index.htm",
        "category": "Later Texts"
    },
    "Dakshinamurti Stotra": {
        "url": "https://www.sacred-texts.com/hin/ds/index.htm",
        "category": "Later Texts"
    },
    "The Sánkhya Aphorisms of Kapila": {
        "url": "https://www.sacred-texts.com/hin/sak/index.htm",
        "category": "Later Texts"
    },
    "Kalidasa: Translations of Shakuntala and Other Works": {
        "url": "https://www.sacred-texts.com/hin/kali/index.htm",
        "category": "Later Texts"
    },
    "The Little Clay Cart": {
        "url": "https://www.sacred-texts.com/hin/lcc/index.htm",
        "category": "Later Texts"
    },
    "Verses of Vemana": {
        "url": "https://www.sacred-texts.com/hin/vov/index.htm",
        "category": "Later Texts"
    },
    "Black Marigolds (Caurapañcāśikā)": {
        "url": "https://www.sacred-texts.com/hin/bm/index.htm",
        "category": "Later Texts"
    },
    "Vikram and the Vampire": {
        "url": "https://www.sacred-texts.com/hin/vv/index.htm",
        "category": "Later Texts"
    },
    "Hymns of the Tamil Saivite Saints": {
        "url": "https://www.sacred-texts.com/hin/htss/index.htm",
        "category": "Later Texts"
    },
    "Songs of Kabîr": {
        "url": "https://www.sacred-texts.com/hin/sok/index.htm",
        "category": "Later Texts"
    },
    "Yoga Vashisht or Heaven Found": {
        "url": "https://www.sacred-texts.com/hin/yvhf/index.htm",
        "category": "Later Texts"
    },
    
    # Modern Books
    "Karma-Yoga": {
        "url": "https://www.sacred-texts.com/hin/kyog/index.htm",
        "category": "Modern Books"
    },
    "Hindu Mysticism": {
        "url": "https://www.sacred-texts.com/hin/hm/index.htm",
        "category": "Modern Books"
    },
    "Writings of Sister Nivedita": {
        "url": "https://www.sacred-texts.com/hin/niv/index.htm",
        "category": "Modern Books"
    },
    "Kali the Mother": {
        "url": "https://www.sacred-texts.com/hin/ktm/index.htm",
        "category": "Modern Books"
    },
    "The Web of Indian Life": {
        "url": "https://www.sacred-texts.com/hin/wil/index.htm",
        "category": "Modern Books"
    },
    "Studies from an Eastern Home": {
        "url": "https://www.sacred-texts.com/hin/seh/index.htm",
        "category": "Modern Books"
    },
    "Writings of Rabindranath Tagore": {
        "url": "https://www.sacred-texts.com/hin/tagore/index.htm",
        "category": "Modern Books"
    },
    "Gitanjali": {
        "url": "https://www.sacred-texts.com/hin/tagore/gitnjali.htm",
        "category": "Modern Books"
    },
    "Saddhana, The Realisation of Life": {
        "url": "https://www.sacred-texts.com/hin/tagore/sadh/index.htm",
        "category": "Modern Books"
    },
    "The Crescent Moon": {
        "url": "https://www.sacred-texts.com/hin/tagore/cresmoon/index.htm",
        "category": "Modern Books"
    },
    "Fruit-Gathering": {
        "url": "https://www.sacred-texts.com/hin/tagore/frutgath.htm",
        "category": "Modern Books"
    },
    "Stray Birds": {
        "url": "https://www.sacred-texts.com/hin/tagore/strybrds.htm",
        "category": "Modern Books"
    },
    "The Home and the World": {
        "url": "https://www.sacred-texts.com/hin/tagore/homewrld/index.htm",
        "category": "Modern Books"
    },
    "Thought Relics": {
        "url": "https://www.sacred-texts.com/hin/tagore/tr/index.htm",
        "category": "Modern Books"
    },
    "The Indian Stories of F.W. Bain": {
        "url": "https://www.sacred-texts.com/hin/bain/index.htm",
        "category": "Modern Books"
    },
}

def get_text_content(scraper, url):
    """Fetch the text content from a URL using cloudscraper"""
    try:
        response = scraper.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_text_from_html(html_content):
    """Extract plain text from HTML content"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Error extracting text from HTML: {e}")
        return None

def fetch_all_texts():
    """Fetch all Hindu texts from sacred-texts.com"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create cloudscraper instance
    scraper = cloudscraper.create_scraper()
    
    # Create metadata file
    metadata = {
        "source": "https://www.sacred-texts.com/hin/index.htm",
        "total_texts": len(HINDU_TEXTS),
        "texts": {}
    }
    
    successful = 0
    failed = 0
    
    for title, info in HINDU_TEXTS.items():
        url = info['url']
        category = info['category']
        
        print(f"Fetching: {title}...")
        
        # Create category directory
        category_dir = os.path.join(OUTPUT_DIR, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Fetch content
        html_content = get_text_content(scraper, url)
        
        if html_content:
            # Extract text
            text_content = extract_text_from_html(html_content)
            
            if text_content:
                # Save to file
                safe_filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                file_path = os.path.join(category_dir, f"{safe_filename}.txt")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                
                # Update metadata
                metadata["texts"][title] = {
                    "url": url,
                    "category": category,
                    "file": file_path,
                    "status": "success"
                }
                
                print(f"✓ Saved: {file_path}")
                successful += 1
            else:
                metadata["texts"][title] = {
                    "url": url,
                    "category": category,
                    "status": "failed - text extraction error"
                }
                failed += 1
        else:
            metadata["texts"][title] = {
                "url": url,
                "category": category,
                "status": "failed - fetch error"
            }
            failed += 1
        
        # Rate limiting to be respectful to the server
        time.sleep(1)
    
    # Save metadata
    metadata_path = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Fetch Complete!")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Total: {successful + failed}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Metadata saved to: {metadata_path}")
    print(f"{'='*60}")

if __name__ == "__main__":
    fetch_all_texts()
