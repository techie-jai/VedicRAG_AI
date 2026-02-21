# Test script for Vedic RAG system
from simple_rag_demo import VedicRAGDemo

def test_rag_system():
    """Test the RAG system with sample queries"""
    print("🕉️ Testing Vedic RAG System...")
    print("=" * 50)
    
    # Initialize the RAG system
    rag = VedicRAGDemo()
    
    # Test queries
    test_queries = [
        "courage",
        "duty and righteousness",
        "wisdom and knowledge",
        "leadership",
        "peace and meditation"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 30)
        
        response = rag.generate_response(query, max_verses=2)
        print(response[:500] + "..." if len(response) > 500 else response)
        
        print("\n" + "="*50)

if __name__ == "__main__":
    test_rag_system()
