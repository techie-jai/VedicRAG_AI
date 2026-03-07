#!/usr/bin/env python3
"""
Test script to verify frontend-backend connection.
Run this to check if the backend API is accessible and working.
"""

import requests
import json
from api_client import check_backend_health, get_backend_status, query_backend

def test_backend_connection():
    """Test the connection to the backend API."""
    print("=" * 60)
    print("Digital Nalanda - Backend Connection Test")
    print("=" * 60)
    
    print("\n1. Checking backend health...")
    is_healthy = check_backend_health()
    
    if is_healthy:
        print("   Status: HEALTHY")
    else:
        print("   Status: OFFLINE or UNREACHABLE")
        print("   Make sure the backend is running on http://localhost:8000")
        print("   To start the backend, run:")
        print("   python -m uvicorn Docker Code.main:app --host 0.0.0.0 --port 8000")
        return
    
    print("\n2. Getting detailed backend status...")
    status = get_backend_status()
    print(f"   Status: {json.dumps(status, indent=2)}")
    
    print("\n3. Testing a sample query...")
    test_query = "What is Brahman according to Vedanta?"
    print(f"   Query: {test_query}")
    
    result = query_backend(test_query, researcher_mode=False)
    
    if result.get("success"):
        print("   Status: SUCCESS")
        print(f"   Answer: {result.get('answer', 'No answer')[:200]}...")
        print(f"   Sources found: {len(result.get('sources', []))}")
        print(f"   Confidence: {result.get('confidence', 0):.0%}")
    else:
        print("   Status: FAILED")
        print(f"   Error: {result.get('answer', 'Unknown error')}")
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_backend_connection()
