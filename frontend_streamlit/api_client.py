import requests
import streamlit as st
from typing import Dict, Any, List
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

def check_backend_health() -> bool:
    """Check if backend is running and healthy."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Backend health check failed: {e}")
        return False

def query_backend(question: str, researcher_mode: bool = False) -> Dict[str, Any]:
    """
    Query the backend RAG API.
    
    Args:
        question: User's question
        researcher_mode: Whether to include detailed scholarly information
        
    Returns:
        Dictionary with answer and sources
    """
    try:
        payload = {
            "question": question
        }
        
        response = requests.post(
            f"{BACKEND_URL}/query",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "answer": data.get("answer", ""),
                "sources": data.get("sources", []),
                "confidence": 0.85
            }
        else:
            return {
                "success": False,
                "answer": f"Backend error: {response.status_code}",
                "sources": [],
                "confidence": 0
            }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "answer": "Cannot connect to backend. Make sure the backend server is running on http://localhost:8000",
            "sources": [],
            "confidence": 0
        }
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "answer": "Backend request timed out. Please try again.",
            "sources": [],
            "confidence": 0
        }
    except Exception as e:
        return {
            "success": False,
            "answer": f"Error querying backend: {str(e)}",
            "sources": [],
            "confidence": 0
        }

def get_backend_status() -> Dict[str, Any]:
    """Get detailed backend status information."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "message": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"status": "offline", "message": str(e)}
