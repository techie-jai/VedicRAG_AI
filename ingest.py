import os
import sys
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
DATA_DIR = Path("./dharmaganj")
INGEST_DB = Path("./ingest_tracker.db")

def init_tracker_db():
    conn = sqlite3.connect(str(INGEST_DB))
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingested_files (
            file_path TEXT PRIMARY KEY,
            file_hash TEXT NOT NULL,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'completed'
        )
    ''')
    conn.commit()
    return conn

def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def find_all_files(directory):
    """Recursively find all .txt and .md files in directory and subdirectories"""
    files = []
    for ext in [".txt", ".md"]:
        files.extend(directory.glob(f"**/*{ext}"))
    return sorted(files)

def get_new_files(conn):
    """Find files in dharmaganj that haven't been ingested yet"""
    cursor = conn.cursor()
    all_files = find_all_files(DATA_DIR)
    
    new_files = []
    for file_path in all_files:
        relative_path = str(file_path.relative_to(DATA_DIR))
        cursor.execute('SELECT file_hash FROM ingested_files WHERE file_path = ?', (relative_path,))
        result = cursor.fetchone()
        
        if result is None:
            new_files.append(file_path)
        else:
            current_hash = get_file_hash(file_path)
            if current_hash != result[0]:
                new_files.append(file_path)
    
    return new_files

def mark_files_ingested(conn, file_paths):
    """Mark files as ingested in the tracker database"""
    cursor = conn.cursor()
    for file_path in file_paths:
        relative_path = str(file_path.relative_to(DATA_DIR))
        file_hash = get_file_hash(file_path)
        cursor.execute('''
            INSERT OR REPLACE INTO ingested_files (file_path, file_hash, status)
            VALUES (?, ?, 'completed')
        ''', (relative_path, file_hash))
    conn.commit()

def main():
    print("=" * 60)
    print("Digital Nalanda - Scripture Ingestion Pipeline")
    print("=" * 60)

    # 1. Ensure directory exists
    if not DATA_DIR.exists():
        print(f"ERROR: Data directory not found at {DATA_DIR.absolute()}")
        sys.exit(1)

    # 2. Initialize tracker database
    tracker_conn = init_tracker_db()

    # 3. Find all files recursively
    print(f"Scanning for files recursively in {DATA_DIR.absolute()}...")
    all_files = find_all_files(DATA_DIR)
    print(f"✓ Found {len(all_files)} total files (.txt and .md)")

    # 4. Find new/modified files
    new_files = get_new_files(tracker_conn)
    
    if not new_files:
        print("✓ No new files to ingest. All files are up to date.")
        tracker_conn.close()
        return
    
    print(f"\n✓ Found {len(new_files)} new/modified files to ingest:")
    for f in new_files:
        print(f"  - {f.relative_to(DATA_DIR)}")

    # 5. Load only new documents
    print(f"\nLoading {len(new_files)} new documents...")
    documents = SimpleDirectoryReader(
        input_dir=str(DATA_DIR), 
        required_exts=[".txt", ".md"],
        recursive=True,
        file_metadata=lambda x: {"file_path": str(x)}
    ).load_data()
    
    if not documents:
        print("No documents could be loaded.")
        tracker_conn.close()
        sys.exit(0)
        
    print(f"✓ Loaded {len(documents)} document pages from new files.")

    # 6. Intelligent Scripture Chunking
    text_parser = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )

    # 7. Initialize ChromaDB
    print(f"\nConnecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}...")
    try:
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        chroma_collection = chroma_client.get_or_create_collection("digital_nalanda")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        print("✓ Successfully connected to ChromaDB.")
    except Exception as e:
        print(f"CRITICAL: Could not connect to ChromaDB. Ensure your docker container is running. Error: {e}")
        tracker_conn.close()
        sys.exit(1)

    # 8. Initialize Embedding Model
    print(f"Initializing Nomic Embeddings via Ollama...")
    embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=OLLAMA_BASE_URL
    )

    # 9. Build the Index (This executes chunking, embedding, and storing)
    print("\nStarting ingestion process (this may take a moment depending on file size)...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        transformations=[text_parser],
        show_progress=True
    )

    # 10. Mark files as ingested
    mark_files_ingested(tracker_conn, new_files)
    tracker_conn.close()

    print("\n" + "=" * 60)
    print(f"✓ Ingestion successful! {len(new_files)} new files processed.")
    print(f"✓ Total embeddings in ChromaDB: {chroma_collection.count()}")
    print("=" * 60)

if __name__ == "__main__":
    main()