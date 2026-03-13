import os
import sys
import requests
import chromadb
from typing import Dict, Any

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
FASTAPI_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8080")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

def test_chroma_connection() -> Dict[str, Any]:
    """Test ChromaDB connection and count embeddings."""
    print("\n" + "="*60)
    print("Testing ChromaDB Connection")
    print("="*60)
    
    try:
        chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        print(f"✓ Connected to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}")
        
        collection = chroma_client.get_or_create_collection("digital_nalanda")
        embedding_count = collection.count()
        
        print(f"✓ Collection 'digital_nalanda' found")
        print(f"✓ Total embeddings in ChromaDB: {embedding_count}")
        
        if embedding_count == 0:
            print("⚠ WARNING: No embeddings found in ChromaDB. Data may not be persisted.")
        else:
            print(f"✓ Data persistence confirmed: {embedding_count} embeddings present")
        
        return {
            "status": "success",
            "embedding_count": embedding_count,
            "host": CHROMA_HOST,
            "port": CHROMA_PORT
        }
    except Exception as e:
        print(f"✗ Failed to connect to ChromaDB: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "host": CHROMA_HOST,
            "port": CHROMA_PORT
        }

def test_fastapi_health() -> Dict[str, Any]:
    """Test FastAPI health endpoint."""
    print("\n" + "="*60)
    print("Testing FastAPI Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✓ FastAPI is healthy")
            print(f"  Service: {health_data.get('service', 'N/A')}")
            print(f"  Ollama URL: {health_data.get('ollama_base_url', 'N/A')}")
            print(f"  ChromaDB: {health_data.get('chroma_host', 'N/A')}:{health_data.get('chroma_port', 'N/A')}")
            return {
                "status": "success",
                "health_data": health_data
            }
        else:
            print(f"✗ FastAPI returned status code: {response.status_code}")
            return {
                "status": "failed",
                "status_code": response.status_code
            }
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Failed to connect to FastAPI at {FASTAPI_BASE_URL}: {e}")
        return {
            "status": "failed",
            "error": f"Connection error: {str(e)}"
        }
    except Exception as e:
        print(f"✗ Error testing FastAPI health: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }

def test_frontend_health() -> Dict[str, Any]:
    """Test if frontend is up and running."""
    print("\n" + "="*60)
    print("Testing Frontend Health Check")
    print("="*60)
    
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print(f"✓ Frontend is up and running at {FRONTEND_URL}")
            return {
                "status": "success",
                "url": FRONTEND_URL,
                "status_code": response.status_code
            }
        else:
            print(f"✗ Frontend returned status code: {response.status_code}")
            return {
                "status": "failed",
                "url": FRONTEND_URL,
                "status_code": response.status_code
            }
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Failed to connect to frontend at {FRONTEND_URL}: {e}")
        return {
            "status": "failed",
            "url": FRONTEND_URL,
            "error": f"Connection error: {str(e)}"
        }
    except Exception as e:
        print(f"✗ Error testing frontend health: {e}")
        return {
            "status": "failed",
            "url": FRONTEND_URL,
            "error": str(e)
        }

def test_llm_query() -> Dict[str, Any]:
    """Test LLM query through FastAPI."""
    print("\n" + "="*60)
    print("Testing LLM Query")
    print("="*60)
    
    question = "What are Vedas & Upnishads"
    print(f"Query: {question}")
    
    try:
        payload = {"question": question}
        response = requests.post(
            f"{FASTAPI_BASE_URL}/query",
            json=payload,
            timeout=300
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ LLM responded successfully")
            print(f"\nAnswer:")
            print("-" * 60)
            print(result.get("answer", "No answer provided"))
            print("-" * 60)
            
            sources = result.get("sources", [])
            print(f"\n✓ Retrieved {len(sources)} source(s):")
            for i, source in enumerate(sources, 1):
                print(f"\n  Source {i}:")
                print(f"  Text: {source.get('text', 'N/A')[:100]}...")
                if source.get('metadata'):
                    print(f"  Metadata: {source.get('metadata')}")
            
            return {
                "status": "success",
                "question": question,
                "answer_length": len(result.get("answer", "")),
                "source_count": len(sources)
            }
        else:
            print(f"✗ Query failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return {
                "status": "failed",
                "status_code": response.status_code,
                "error": response.text
            }
    except requests.exceptions.Timeout:
        print(f"✗ Query timed out after 300 seconds")
        return {
            "status": "failed",
            "error": "Query timeout"
        }
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Failed to connect to FastAPI: {e}")
        return {
            "status": "failed",
            "error": f"Connection error: {str(e)}"
        }
    except Exception as e:
        print(f"✗ Error during query: {e}")
        return {
            "status": "failed",
            "error": str(e)
        }

def main():
    """Run all frontend and backend tests."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  VEDIC RAG AI - FRONTEND & BACKEND TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print(f"\nConfiguration:")
    print(f"  Frontend URL: {FRONTEND_URL}")
    print(f"  FastAPI URL: {FASTAPI_BASE_URL}")
    print(f"  Ollama URL: {OLLAMA_BASE_URL}")
    print(f"  ChromaDB: {CHROMA_HOST}:{CHROMA_PORT}")
    
    results = {
        "frontend": test_frontend_health(),
        "chroma": test_chroma_connection(),
        "fastapi_health": test_fastapi_health(),
        "llm_query": test_llm_query()
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    all_passed = True
    for test_name, result in results.items():
        status = result.get("status", "unknown")
        symbol = "✓" if status == "success" else "✗"
        print(f"{symbol} {test_name}: {status}")
        if status != "success":
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✓ All tests passed! Frontend and Backend are working properly.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
