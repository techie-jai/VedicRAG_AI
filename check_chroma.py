import chromadb
import os
import sys

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

print("=" * 60)
print("ChromaDB Data Persistence Check")
print("=" * 60)

try:
    print(f"\nConnecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}...")
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    
    # List all collections
    print("\nFetching all collections...")
    collections = chroma_client.list_collections()
    print(f"Total collections found: {len(collections)}")
    
    if len(collections) == 0:
        print("❌ NO COLLECTIONS FOUND - Data is NOT persisting!")
    else:
        print("\nCollections:")
        for collection in collections:
            print(f"  - {collection.name}")
    
    # Check the specific collection we use
    print(f"\nChecking 'digital_nalanda' collection...")
    try:
        chroma_collection = chroma_client.get_collection("digital_nalanda")
        count = chroma_collection.count()
        print(f"✓ Collection exists with {count} embeddings")
        
        if count == 0:
            print("❌ Collection is EMPTY - Data is NOT persisting!")
        else:
            print(f"✓ Data IS persisting! {count} embeddings found.")
            
            # Show a sample
            print(f"\nSample of stored data (first 3 items):")
            results = chroma_collection.get(limit=3)
            for i, doc_id in enumerate(results['ids'][:3]):
                print(f"  {i+1}. ID: {doc_id}")
                if results['documents']:
                    print(f"     Document: {results['documents'][i][:100]}...")
                    
    except Exception as e:
        print(f"❌ Collection 'digital_nalanda' does not exist: {e}")
        
except Exception as e:
    print(f"❌ ERROR: Could not connect to ChromaDB: {e}")
    print(f"   Make sure ChromaDB is running at {CHROMA_HOST}:{CHROMA_PORT}")
    sys.exit(1)

print("\n" + "=" * 60)
