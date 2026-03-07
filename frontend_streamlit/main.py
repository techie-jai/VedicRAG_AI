import streamlit as st
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from api_client import query_backend, check_backend_health, get_backend_status

st.set_page_config(
    page_title="Digital Nalanda",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_vector_db():
    """
    Initialize the vector database connection.
    Placeholder for actual implementation.
    """
    return {"status": "initialized", "documents_indexed": 0}

def get_rag_response(query: str, researcher_mode: bool = False) -> Dict[str, Any]:
    """
    Get RAG response from the backend API.
    
    Args:
        query: User query
        researcher_mode: If True, return detailed scholarly information
        
    Returns:
        Dictionary containing response, sources, and confidence score
    """
    result = query_backend(query, researcher_mode)
    
    return {
        "response": result.get("answer", ""),
        "sources": result.get("sources", []),
        "overall_confidence": result.get("confidence", 0),
        "query": query,
        "success": result.get("success", False)
    }

def load_custom_css():
    """Load custom CSS for premium academic styling with Bhagwa (saffron) accents."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #1a1a1a;
        color: #F5F5F5;
    }
    
    [data-testid="stSidebar"] {
        background-color: #2d2d2d;
        border-right: 3px solid #FF9933;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Crimson Text', serif !important;
        color: #F5F5F5;
        letter-spacing: 0.5px;
        line-height: 1.4;
    }
    
    h1 {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        font-size: 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        color: #FF9933;
    }
    
    h3 {
        font-size: 1.3rem;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
        color: #FF9933;
    }
    
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
        color: #F5F5F5;
        line-height: 1.6;
    }
    
    [data-testid="stChatMessage"] {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border-left: 4px solid #FF9933;
        line-height: 1.6;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    [data-testid="stChatMessage"] p {
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #3d3d3d;
        border-left-color: #FF9933;
        margin-left: 2rem;
        margin-right: 0;
    }
    
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background-color: #252525;
        border-left-color: #FF9933;
        margin-right: 2rem;
        margin-left: 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #3d3d3d;
        color: #F5F5F5;
        border: 2px solid #FF9933;
        border-radius: 6px;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
        line-height: 1.5;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FF9933;
        box-shadow: 0 0 0 3px rgba(255, 153, 51, 0.2);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #FF9933 0%, #FFB366 100%);
        color: #1a1a1a;
        border: none;
        border-radius: 6px;
        padding: 0.7rem 1.8rem;
        font-weight: 700;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFB366 0%, #FFCC99 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(255, 153, 51, 0.4);
    }
    
    .stExpander {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 6px;
    }
    
    .stExpander > div > div > button {
        color: #FF9933;
        font-weight: 600;
    }
    
    .stSelectbox > div > div {
        background-color: #3d3d3d;
        border: 1px solid #FF9933;
        border-radius: 6px;
    }
    
    .stCheckbox > label {
        color: #F5F5F5;
        line-height: 1.6;
    }
    
    .stCheckbox > label > div {
        background-color: #3d3d3d;
        border: 2px solid #FF9933;
        border-radius: 4px;
    }
    
    .metric-card {
        background-color: #2d2d2d;
        border: 1px solid #FF9933;
        border-radius: 8px;
        padding: 1.25rem;
        margin: 0.75rem 0;
        line-height: 1.6;
    }
    
    .source-item {
        background-color: #252525;
        border-left: 4px solid #FF9933;
        padding: 1.25rem;
        margin: 1rem 0;
        border-radius: 4px;
        line-height: 1.6;
    }
    
    .source-item p {
        margin: 0.5rem 0;
    }
    
    .sanskrit-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.2rem;
        color: #FF9933;
        font-style: italic;
        margin: 0.75rem 0;
        line-height: 1.6;
    }
    
    .confidence-badge {
        display: inline-block;
        background: linear-gradient(135deg, #FF9933 0%, #FFB366 100%);
        color: #1a1a1a;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-left: 0.5rem;
    }
    
    .sample-question {
        background-color: #3d3d3d;
        border: 2px solid #FF9933;
        border-radius: 6px;
        padding: 1.25rem;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        font-size: 0.9rem;
        line-height: 1.5;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .sample-question:hover {
        background: linear-gradient(135deg, #3d3d3d 0%, #4d4d4d 100%);
        border-color: #FFB366;
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(255, 153, 51, 0.3);
    }
    
    .divider {
        height: 2px;
        background: linear-gradient(to right, transparent, #FF9933, transparent);
        margin: 1.5rem 0;
    }
    
    .sidebar-section {
        background-color: #252525;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        border: 1px solid #3d3d3d;
        border-top: 3px solid #FF9933;
        line-height: 1.6;
    }
    
    .sidebar-title {
        color: #FF9933;
        font-weight: 700;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    
    .sidebar-section p {
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with project information and navigation."""
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Digital Nalanda</div>', unsafe_allow_html=True)
        st.markdown("""
        A RAG-based AI system trained on ancient Indian scriptures—
        Vedas, Upanishads, and classical philosophical texts.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Settings</div>', unsafe_allow_html=True)
        
        researcher_mode = st.checkbox(
            "Researcher Mode",
            value=False,
            help="Enable detailed scholarly information with Sanskrit shlokas and commentaries"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
        
        nav_option = st.radio(
            "Select a section:",
            ["Chat", "Browse Scriptures", "About"],
            label_visibility="collapsed"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Backend Status</div>', unsafe_allow_html=True)
        
        backend_status = get_backend_status()
        status_color = "green" if backend_status.get("status") == "healthy" else "red"
        st.markdown(f"**Status:** <span style='color: {status_color};'>{backend_status.get('status', 'unknown')}</span>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">Project Info</div>', unsafe_allow_html=True)
        st.markdown("""
        **Version:** 1.0.0  
        **Vector DB:** ChromaDB  
        **Model:** Ollama LLM  
        **Scriptures:** 50+ texts indexed
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        return researcher_mode, nav_option

def render_sample_questions():
    """Render a grid of sample questions."""
    st.markdown("### Sample Questions")
    st.markdown("Click any question to explore:")
    
    sample_questions = [
        "What is Brahman according to Vedanta?",
        "Explain the concept of Karma and Dharma",
        "What are the four Vedas?",
        "Define Moksha in Hindu philosophy",
        "What is the Bhagavad Gita's core message?",
        "Explain the Upanishadic teachings on Atman"
    ]
    
    cols = st.columns(2)
    for idx, question in enumerate(sample_questions):
        with cols[idx % 2]:
            if st.button(question, key=f"sample_{idx}", use_container_width=True):
                st.session_state.user_input = question
                st.rerun()

def render_chat_interface(researcher_mode: bool):
    """Render the main chat interface."""
    st.markdown("### Chat with Digital Nalanda")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("Sources & Confidence"):
                        overall_conf = message.get("confidence", 0)
                        st.markdown(f"**Overall Confidence:** {overall_conf:.0%}")
                        
                        st.markdown("---")
                        
                        for idx, source in enumerate(message["sources"], 1):
                            st.markdown(f'<div class="source-item">', unsafe_allow_html=True)
                            
                            if "text" in source:
                                st.markdown(f'<div class="sanskrit-text">{source["text"]}</div>', unsafe_allow_html=True)
                            
                            if "transliteration" in source:
                                st.markdown(f"**Transliteration:** {source['transliteration']}")
                            
                            if "source" in source:
                                st.markdown(f"**Source:** {source['source']}")
                            
                            if "confidence" in source:
                                confidence_pct = f"{source['confidence']:.0%}"
                                st.markdown(
                                    f'<span class="confidence-badge">{confidence_pct}</span>',
                                    unsafe_allow_html=True
                                )
                            
                            if researcher_mode and "commentary" in source:
                                st.markdown(f"**Commentary:** {source['commentary']}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 0.15])
    
    with col1:
        user_input = st.text_input(
            "Ask a question about the scriptures...",
            key="user_input",
            placeholder="What would you like to know about Vedic philosophy?"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True, key="send_btn")
    
    if send_button and user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        with st.spinner("Searching scriptures..."):
            rag_response = get_rag_response(user_input, researcher_mode)
        
        assistant_message = {
            "role": "assistant",
            "content": rag_response["response"],
            "sources": rag_response.get("sources", []),
            "confidence": rag_response.get("overall_confidence", 0)
        }
        
        st.session_state.messages.append(assistant_message)
        st.rerun()

def render_browse_scriptures():
    """Render the scripture browsing interface."""
    st.markdown("### Browse Scriptures")
    
    scripture_categories = {
        "Vedas": ["Rigveda", "Yajurveda", "Samaveda", "Atharvaveda"],
        "Upanishads": ["Isha Upanishad", "Kena Upanishad", "Katha Upanishad", "Mundaka Upanishad"],
        "Brahma Sutras": ["Adhyaya 1", "Adhyaya 2", "Adhyaya 3", "Adhyaya 4"],
        "Bhagavad Gita": ["Chapter 1-6", "Chapter 7-12", "Chapter 13-18"]
    }
    
    selected_category = st.selectbox("Select a category:", list(scripture_categories.keys()))
    
    if selected_category:
        st.markdown(f"**{selected_category}**")
        cols = st.columns(2)
        for idx, text in enumerate(scripture_categories[selected_category]):
            with cols[idx % 2]:
                st.button(text, use_container_width=True, key=f"scripture_{idx}")

def render_about():
    """Render the about page."""
    st.markdown("### About Digital Nalanda")
    
    st.markdown("""
    **Digital Nalanda** is a cutting-edge RAG (Retrieval-Augmented Generation) system 
    designed to make ancient Indian scriptures accessible through modern AI technology.
    
    #### Mission
    To preserve, index, and make searchable the wisdom of ancient Indian philosophical texts,
    enabling scholars, students, and seekers to explore Vedic knowledge with precision and depth.
    
    #### Indexed Scriptures
    - **Vedas:** Rigveda, Yajurveda, Samaveda, Atharvaveda
    - **Upanishads:** 108 principal Upanishads
    - **Brahma Sutras:** Complete with Shankara Bhashya
    - **Bhagavad Gita:** With multiple commentaries
    - **Classical Texts:** Brahma Sutras, Yoga Sutras, and more
    
    #### Technology Stack
    - **Vector Database:** ChromaDB
    - **LLM:** Ollama (Local LLM)
    - **Frontend:** Streamlit
    - **Backend:** Python FastAPI
    - **Embedding Model:** Ollama Embeddings
    
    #### Team
    Built with dedication to preserving and democratizing Vedic knowledge.
    """)

def main():
    """Main application entry point."""
    load_custom_css()
    
    researcher_mode, nav_option = render_sidebar()
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1>Digital Nalanda</h1>
        <p style="color: #FF9933; font-size: 1.1rem; margin-top: 0.5rem;">
            Exploring Ancient Wisdom Through Modern AI
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    if nav_option == "Chat":
        render_sample_questions()
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        render_chat_interface(researcher_mode)
    
    elif nav_option == "Browse Scriptures":
        render_browse_scriptures()
    
    elif nav_option == "About":
        render_about()

if __name__ == "__main__":
    main()
