# Simple Vedic RAG Demo
# A basic demonstration of the RAG system using the generated Vedic dataset

import os
import json
from typing import List, Dict, Any
import re

class VedicRAGDemo:
    def __init__(self, dataset_dir: str = "vedic_texts"):
        self.dataset_dir = dataset_dir
        self.verses = []
        self.load_dataset()
    
    def load_dataset(self):
        """Load the vedic dataset from text files"""
        print("Loading Vedic dataset...")
        
        # Load metadata
        metadata_path = os.path.join(self.dataset_dir, "dataset_metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
                print(f"Dataset contains {self.metadata['total_verses']} verses")
        
        # Load verses from text files
        for filename in os.listdir(self.dataset_dir):
            if filename.startswith("vedic_corpus_part_") and filename.endswith(".txt"):
                file_path = os.path.join(self.dataset_dir, filename)
                self.load_verses_from_file(file_path)
        
        print(f"Loaded {len(self.verses)} verses into memory")
    
    def load_verses_from_file(self, file_path: str):
        """Load verses from a single text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by --- to get individual verses
        verse_blocks = content.split('---')
        
        for block in verse_blocks:
            if block.strip():
                verse = self.parse_verse_block(block.strip())
                if verse:
                    self.verses.append(verse)
    
    def parse_verse_block(self, block: str) -> Dict[str, Any]:
        """Parse a verse block into structured data"""
        verse = {}
        lines = block.split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                verse[key.strip().lower()] = value.strip()
        
        return verse if verse else None
    
    def search_verses(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search for verses"""
        query_lower = query.lower()
        relevant_verses = []
        
        for verse in self.verses:
            score = 0
            
            # Simple scoring based on keyword matches
            if 'english' in verse:
                english_words = verse['english'].lower().split()
                query_words = query_lower.split()
                
                for query_word in query_words:
                    if query_word in english_words:
                        score += 1
            
            # Also check category and source
            if 'category' in verse and query_lower in verse['category'].lower():
                score += 2
            if 'source' in verse and query_lower in verse['source'].lower():
                score += 2
            
            if score > 0:
                verse_copy = verse.copy()
                verse_copy['relevance_score'] = score
                relevant_verses.append(verse_copy)
        
        # Sort by relevance score and return top results
        relevant_verses.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        return relevant_verses[:max_results]
    
    def generate_response(self, query: str, max_verses: int = 3) -> str:
        """Generate a response using retrieved verses"""
        relevant_verses = self.search_verses(query, max_verses)
        
        if not relevant_verses:
            return "I couldn't find relevant verses for your query. Please try different keywords."
        
        response = f"🕉️ Based on your query about '{query}', here are some relevant teachings from the Vedic scriptures:\n\n"
        
        for i, verse in enumerate(relevant_verses, 1):
            response += f"**{i}. {verse.get('title', 'Unknown')}**\n"
            response += f"Source: {verse.get('source', 'Unknown')} ({verse.get('category', 'Unknown')})\n\n"
            response += f"**Sanskrit:**\n{verse.get('sanskrit', 'N/A')}\n\n"
            response += f"**English Translation:**\n{verse.get('english', 'N/A')}\n\n"
            response += "---\n\n"
        
        response += "**Reflection:**\n"
        response += "These verses offer timeless wisdom that can be applied to modern life. "
        response += "Consider how these teachings relate to your situation and contemplate their deeper meaning.\n\n"
        response += "Would you like me to search for verses on a different topic or explore another aspect of Vedic wisdom?"
        
        return response
    
    def interactive_demo(self):
        """Run an interactive demo"""
        print("🕉️ Welcome to the Vedic Wisdom RAG Demo!")
        print("=" * 50)
        print("Ask questions about life, duty, wisdom, or any topic.")
        print("Type 'quit' to exit.\n")
        
        while True:
            query = input("💭 What would you like to know about Vedic wisdom? ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n🙏 Thank you for exploring Vedic wisdom. May you find peace and guidance!")
                break
            
            if not query:
                continue
            
            print("\n" + "="*50)
            response = self.generate_response(query)
            print(response)
            print("="*50 + "\n")

def main():
    """Main function to run the demo"""
    # Check if dataset exists
    if not os.path.exists("vedic_texts"):
        print("❌ Dataset not found! Please run VedicDatasetGenerator.py first.")
        return
    
    # Initialize and run the RAG demo
    rag = VedicRAGDemo()
    rag.interactive_demo()

if __name__ == "__main__":
    main()
