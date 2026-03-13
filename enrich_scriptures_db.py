import sqlite3
from pathlib import Path
from difflib import SequenceMatcher
import chromadb

def remove_common_suffixes(text):
    """
    Remove common Sanskrit text suffixes to improve matching
    Helps avoid false positives when multiple texts share the same suffix
    """
    common_suffixes = [
        'purana', 'veda', 'sutra', 'samhita', 'shastra', 'gita', 'upanishad',
        'sutras', 'vedas', 'puranas', 'samhitas', 'shastras', 'gitas', 'upanishads',
        'tantra', 'agama', 'brahman', 'yoga', 'philosophy', 'commentary',
        'part', 'sbe', 'sanskrit', 'principal', 'minor', 'texts', 'hymns'
    ]
    
    text_lower = text.lower()
    words = text_lower.split()
    
    # Remove common suffixes from the end
    while words and words[-1] in common_suffixes:
        words.pop()
    
    return ' '.join(words) if words else text_lower

def fuzzy_match(title, filename, threshold=0.6):
    """
    Perform fuzzy matching between title and filename
    Removes common suffixes before matching to avoid false positives
    Returns match score (0-1)
    """
    # Remove common suffixes first
    title_cleaned = remove_common_suffixes(title)
    filename_cleaned = remove_common_suffixes(filename)
    
    # Normalize for comparison
    title_normalized = title_cleaned.lower().replace(' ', '').replace('-', '')
    filename_normalized = filename_cleaned.lower().replace(' ', '').replace('-', '').replace('.txt', '').replace('.md', '').replace('.xml', '')
    
    ratio = SequenceMatcher(None, title_normalized, filename_normalized).ratio()
    return ratio

def find_scripture_in_dharmaganj(title):
    """
    Search for scripture in dharmaganj folder using fuzzy matching
    Returns tuple: (found, file_name, file_location, score)
    Only returns True if confidence score >= 0.50 (50%)
    """
    dharmaganj_path = Path('dharmaganj')
    
    if not dharmaganj_path.exists():
        return False, None, None, 0
    
    best_match_score = 0
    best_match_file = None
    best_match_name = None
    
    for file_path in dharmaganj_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.xml']:
            filename = file_path.stem
            match_score = fuzzy_match(title, filename)
            
            if match_score > best_match_score:
                best_match_score = match_score
                best_match_file = str(file_path)
                best_match_name = file_path.name
    
    # Only return True if confidence >= 50%
    if best_match_score >= 0.50:
        print(f"  ✓ Found: {title} -> {best_match_file} (score: {best_match_score:.2f})")
        return True, best_match_name, best_match_file, best_match_score
    
    return False, None, None, best_match_score

def check_embeddings_in_chromadb(title):
    """
    Check if embeddings exist in ChromaDB for a given title
    Uses partial matching on metadata
    """
    try:
        client = chromadb.HttpClient(host="localhost", port=8000)
        collections = client.list_collections()
        
        if not collections:
            return False
        
        title_normalized = title.lower()
        
        for collection in collections:
            try:
                col = client.get_collection(name=collection.name)
                results = col.get()
                
                if results and results['metadatas']:
                    for metadata in results['metadatas']:
                        if metadata:
                            metadata_str = str(metadata).lower()
                            if title_normalized in metadata_str or fuzzy_match(title, metadata_str) > 0.7:
                                print(f"  ✓ Embeddings found in collection: {collection.name}")
                                return True
            except Exception as e:
                continue
        
        return False
    
    except Exception as e:
        print(f"  ⚠ ChromaDB connection error: {str(e)}")
        return False

def enrich_scriptures_database():
    """
    Main function to enrich the scriptures database with source and embeddings info
    Assumes columns already exist in the database
    """
    print("=" * 80)
    print("ENRICHING SCRIPTURES DATABASE")
    print("=" * 80)
    
    conn = sqlite3.connect('scriptures.db')
    cursor = conn.cursor()
    
    print("\n[Processing] Reading scriptures and checking sources/embeddings...")
    cursor.execute("SELECT id, title FROM scriptures ORDER BY CAST(rank AS INTEGER)")
    scriptures = cursor.fetchall()
    
    total = len(scriptures)
    source_found = 0
    embeddings_found = 0
    
    print(f"Total scriptures to process: {total}\n")
    
    for idx, (scripture_id, title) in enumerate(scriptures, 1):
        print(f"[{idx}/{total}] {title}")
        
        source_available, file_name, file_location, score = find_scripture_in_dharmaganj(title)
        if source_available:
            source_found += 1
        
        embeddings_available = check_embeddings_in_chromadb(title)
        if embeddings_available:
            embeddings_found += 1
        
        cursor.execute(
            "UPDATE scriptures SET source_data_available = ?, embeddings_generated = ?, file_name = ?, file_location = ? WHERE id = ?",
            (1 if source_available else 0, 1 if embeddings_available else 0, file_name, file_location, scripture_id)
        )
        
        print()
    
    conn.commit()
    
    print("=" * 80)
    print("ENRICHMENT SUMMARY")
    print("=" * 80)
    print(f"Total Scriptures: {total}")
    print(f"Source Data Available: {source_found} ({source_found/total*100:.1f}%)")
    print(f"Embeddings Generated: {embeddings_found} ({embeddings_found/total*100:.1f}%)")
    
    print("\n" + "=" * 80)
    print("SAMPLE RECORDS (First 10)")
    print("=" * 80)
    cursor.execute(
        "SELECT id, title, source_data_available, embeddings_generated, file_name FROM scriptures LIMIT 10"
    )
    
    print(f"{'ID':<5} {'Title':<35} {'Source':<10} {'Embeddings':<12} {'File':<25}")
    print("-" * 100)
    for record in cursor.fetchall():
        source_status = "✓ Yes" if record[2] else "✗ No"
        embeddings_status = "✓ Yes" if record[3] else "✗ No"
        file_name = record[4] if record[4] else "N/A"
        print(f"{record[0]:<5} {record[1]:<35} {source_status:<10} {embeddings_status:<12} {file_name:<25}")
    
    conn.close()
    print("\n✓ Database enrichment complete!")

if __name__ == "__main__":
    enrich_scriptures_database()
