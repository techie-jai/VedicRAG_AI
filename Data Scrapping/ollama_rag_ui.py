import streamlit as st
import os
import json
import requests
from typing import List, Dict, Any
from simple_rag_demo import VedicRAGDemo

st.set_page_config(
    page_title="🕉️ Vedic RAG with Ollama",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .verse-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        border-radius: 0.25rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_rag_system():
    """Load the RAG system once"""
    if not os.path.exists("vedic_texts"):
        return None
    return VedicRAGDemo()

def check_ollama_connection(base_url: str) -> bool:
    """Check if Ollama server is running"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_ollama_models(base_url: str) -> List[str]:
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
    except:
        pass
    return []

def query_ollama(model: str, prompt: str, base_url: str) -> str:
    """Query Ollama model with streaming response"""
    try:
        response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.7,
            },
            timeout=60
        )
        if response.status_code == 200:
            return response.json().get('response', 'No response generated')
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.Timeout:
        return "Error: Request timeout. Ollama server may be slow or unresponsive."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🕉️ Vedic RAG with Ollama")
    st.markdown("*Explore ancient Vedic wisdom with modern AI*")
    
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        ollama_url = st.text_input(
            "Ollama Server URL",
            value="http://localhost:11434",
            help="Enter the URL of your Ollama server"
        )
        
        is_connected = check_ollama_connection(ollama_url)
        if is_connected:
            st.success("✅ Connected to Ollama")
        else:
            st.error("❌ Cannot connect to Ollama. Make sure it's running.")
        
        available_models = get_ollama_models(ollama_url) if is_connected else []
        
        if available_models:
            selected_model = st.selectbox(
                "Select Model",
                available_models,
                help="Choose which Ollama model to use"
            )
        else:
            st.warning("No models found. Pull a model in Ollama first (e.g., `ollama pull mistral`)")
            selected_model = None
        
        st.divider()
        
        st.subheader("RAG Settings")
        max_verses = st.slider(
            "Max Verses to Retrieve",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of relevant verses to include in context"
        )
        
        use_rag = st.checkbox(
            "Use RAG Context",
            value=True,
            help="Include Vedic verses in the prompt for context-aware responses"
        )
        
        st.divider()
        
        st.subheader("About")
        st.markdown("""
        This application combines:
        - **Vedic RAG**: Retrieves relevant verses from Vedic texts
        - **Ollama**: Local LLM for generating responses
        - **Streamlit**: Modern web interface
        
        **How it works:**
        1. Enter your question
        2. System retrieves relevant Vedic verses
        3. Ollama generates a response using the verses as context
        """)

    rag_system = load_rag_system()
    
    if not rag_system:
        st.error("❌ Vedic dataset not found! Please run VedicDatasetGenerator.py first.")
        return
    
    if not is_connected or not selected_model:
        st.warning("⚠️ Please configure Ollama connection and select a model to proceed.")
        return
    
    col1, col2 = st.columns([3, 1])
    with col1:
        user_query = st.text_input(
            "💭 Ask about Vedic wisdom:",
            placeholder="e.g., What does the Bhagavad Gita say about duty?",
            help="Enter your question about Vedic teachings"
        )
    with col2:
        submit_button = st.button("🔍 Search", use_container_width=True)
    
    if submit_button and user_query:
        with st.spinner("🔄 Processing your query..."):
            st.divider()
            
            if use_rag:
                st.subheader("📚 Retrieved Vedic Verses")
                relevant_verses = rag_system.search_verses(user_query, max_verses)
                
                if relevant_verses:
                    for i, verse in enumerate(relevant_verses, 1):
                        with st.container():
                            st.markdown(f"**{i}. {verse.get('title', 'Unknown')}**")
                            st.markdown(f"*Source: {verse.get('source', 'Unknown')} ({verse.get('category', 'Unknown')})*")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Sanskrit:**")
                                st.text(verse.get('sanskrit', 'N/A'))
                            with col2:
                                st.markdown("**English Translation:**")
                                st.text(verse.get('english', 'N/A'))
                            st.divider()
                
                context = "\n\n".join([
                    f"From {v.get('source', 'Unknown')}:\n{v.get('english', 'N/A')}"
                    for v in relevant_verses
                ])
                
                prompt = f"""You are an expert in Vedic philosophy and wisdom. Based on the following Vedic verses, answer the user's question thoughtfully and authentically.

VEDIC CONTEXT:
{context}

USER QUESTION: {user_query}

Provide a comprehensive answer that:
1. References the verses provided
2. Explains their relevance to the question
3. Offers practical wisdom for modern life
4. Maintains the spiritual essence of the teachings"""
            else:
                prompt = f"""You are an expert in Vedic philosophy and wisdom. Answer the following question about Vedic teachings:

QUESTION: {user_query}

Provide a comprehensive, thoughtful answer that reflects authentic Vedic wisdom."""
            
            st.subheader("🤖 Ollama Response")
            response = query_ollama(selected_model, prompt, ollama_url)
            
            st.markdown(response)
            
            st.divider()
            
            if st.button("💾 Save Conversation"):
                conversation = {
                    "query": user_query,
                    "model": selected_model,
                    "response": response,
                    "verses_used": len(relevant_verses) if use_rag else 0
                }
                
                log_file = "conversations.jsonl"
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(conversation, ensure_ascii=False) + "\n")
                
                st.success("✅ Conversation saved!")

if __name__ == "__main__":
    main()
