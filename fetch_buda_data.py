#!/usr/bin/env python3
"""
BUDA API Integration Script for Vedic RAG AI
Fetches relevant Sanskrit texts from Buddhist Digital Resource Center (BUDA)
and categorizes them into dharmaganj structure.
"""

import requests
import json
import time
import os
import re
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote

class BudaAPIClient:
    """Client for BUDA LDS-PDI API"""
    
    def __init__(self):
        self.base_url = "http://purl.bdrc.io"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Vedic-RAG-AI-Integration/1.0',
            'Accept': 'application/json'
        })
    
    def get_queries_list(self) -> List[Dict]:
        """Get list of available query templates"""
        try:
            response = self.session.get(f"{self.base_url}/queries")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching queries: {e}")
            return []
    
    def get_etext_contents(self, search_term: str, lang: str = "sa-x-iast", limit: int = 50) -> Optional[Dict]:
        """
        Search for e-text contents using Etexts_contents query template
        
        Args:
            search_term: Term to search for
            lang: Language code (sa-x-iast for Sanskrit in IAST transliteration)
            limit: Maximum results per page
        """
        try:
            # URL encode the search term
            encoded_term = quote(f'"{search_term}"')
            params = {
                'L_NAME': encoded_term,
                'lang': lang,
                'pageSize': limit
            }
            
            url = f"{self.base_url}/query/table/Etexts_contents"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error searching for '{search_term}': {e}")
            return None
    
    def get_resource_info(self, resource_id: str) -> Optional[Dict]:
        """Get detailed information about a specific resource"""
        try:
            url = f"{self.base_url}/resource/{resource_id}"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching resource {resource_id}: {e}")
            return None

class DharmaganjCategorizer:
    """Categorizes BUDA content into dharmaganj structure"""
    
    # Keywords and patterns for each building/domain
    CATEGORIES = {
        "ratnodadhi": {
            "shruti": ["veda", "rig", "sama", "yajur", "atharva", "samhita"],
            "sutra": ["sutra", "prajnaparamita", "guhyasamaja", "mahayana", "bodhicitta"],
            "upanishad": ["upanishad", "upanisad", "brahmana", "aranyaka"]
        },
        "ratnasagara": {
            "cikitsavidya": ["ayurveda", "caraka", "susruta", "medicine", "cikitsa", "dhatu", "rasa"],
            "nyaya_pramana": ["nyaya", "pramana", "logic", "dignaga", "dharmakirti", "tarka"],
            "vyakarana": ["grammar", "panini", "ashtadhyayi", "vyakarana", "sandra"],
            "jyotisha": ["astronomy", "jyotisha", "aryabhata", "planet", "time"],
            "arthashastra": ["arthashastra", "politics", "economics", "kautilya", "statecraft"]
        },
        "ratnaranjaka": {
            "itihasa": ["itihasa", "mahabharata", "ramayana", "epic", "history"],
            "purana": ["purana", "bhagavata", "vishnu", "shiva", "brahma"],
            "kavya": ["kavya", "poetry", "kalidasa", "drama", "nataka", "campu"],
            "vividha": ["music", "art", "culture", "literature", "secular"]
        }
    }
    
    @staticmethod
    def categorize_text(title: str, content: str) -> Tuple[str, str]:
        """
        Categorize a text based on title and content
        
        Returns:
            Tuple of (building, domain)
        """
        title_lower = title.lower()
        content_lower = content.lower()
        combined_text = f"{title_lower} {content_lower}"
        
        # Score each category
        scores = {}
        for building, domains in DharmaganjCategorizer.CATEGORIES.items():
            building_score = 0
            best_domain = None
            best_domain_score = 0
            
            for domain, keywords in domains.items():
                domain_score = 0
                for keyword in keywords:
                    if keyword in title_lower:
                        domain_score += 3  # Title matches are worth more
                    if keyword in content_lower:
                        domain_score += 1
                
                building_score += domain_score
                if domain_score > best_domain_score:
                    best_domain = domain
                    best_domain_score = domain_score
            
            if building_score > 0:
                scores[building] = {
                    'score': building_score,
                    'domain': best_domain
                }
        
        if not scores:
            return "ratnaranjaka", "vividha"  # Default fallback
        
        # Return building with highest score
        best_building = max(scores.keys(), key=lambda k: scores[k]['score'])
        return best_building, scores[best_building]['domain']

class BudaDataFetcher:
    """Main class for fetching and organizing BUDA data"""
    
    def __init__(self, output_dir: str = "dharmaganj"):
        self.client = BudaAPIClient()
        self.output_dir = output_dir
        self.catalog_file = os.path.join(output_dir, "bagdevibhandar", "master_catalog.json")
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Create necessary directories"""
        dirs = [
            "dharmaganj/ratnodadhi/shruti/raw",
            "dharmaganj/ratnodadhi/sutra/raw", 
            "dharmaganj/ratnodadhi/upanishad/raw",
            "dharmaganj/ratnasagara/cikitsavidya/raw",
            "dharmaganj/ratnasagara/nyaya_pramana/raw",
            "dharmaganj/ratnasagara/vyakarana/raw",
            "dharmaganj/ratnasagara/jyotisha/raw",
            "dharmaganj/ratnasagara/arthashastra/raw",
            "dharmaganj/ratnaranjaka/itihasa/raw",
            "dharmaganj/ratnaranjaka/purana/raw",
            "dharmaganj/ratnaranjaka/kavya/raw",
            "dharmaganj/ratnaranjaka/vividha/raw"
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
    
    def search_and_categorize(self, search_terms: List[str]) -> Dict:
        """
        Search BUDA for multiple terms and categorize results
        
        Args:
            search_terms: List of Sanskrit terms to search for
            
        Returns:
            Dictionary with categorized results
        """
        all_results = {
            'ratnodadhi': {'shruti': [], 'sutra': [], 'upanishad': []},
            'ratnasagara': {'cikitsavidya': [], 'nyaya_pramana': [], 'vyakarana': [], 
                          'jyotisha': [], 'arthashastra': []},
            'ratnaranjaka': {'itihasa': [], 'purana': [], 'kavya': [], 'vividha': []}
        }
        
        for term in search_terms:
            print(f"🔍 Searching for: {term}")
            results = self.client.get_etext_contents(term)
            
            if not results or 'results' not in results:
                print(f"❌ No results for '{term}'")
                continue
            
            print(f"📊 Found {len(results['results'])} results for '{term}'")
            
            for item in results['results']:
                resource_id = item.get('resource', '')
                content = item.get('content', '')
                score = item.get('score', 0)
                
                # Get detailed resource info for better categorization
                resource_info = self.client.get_resource_info(resource_id)
                title = resource_info.get('title', resource_id) if resource_info else resource_id
                
                # Categorize the text
                building, domain = DharmaganjCategorizer.categorize_text(title, content)
                
                categorized_item = {
                    'resource_id': resource_id,
                    'title': title,
                    'content': content,
                    'score': score,
                    'search_term': term,
                    'source': 'BUDA'
                }
                
                all_results[building][domain].append(categorized_item)
                print(f"📚 Categorized: {title[:50]}... -> {building}/{domain}")
            
            # Rate limiting
            time.sleep(1)
        
        return all_results
    
    def save_results(self, results: Dict):
        """Save categorized results to appropriate files"""
        metadata_updates = []
        
        for building, domains in results.items():
            for domain, items in domains.items():
                if not items:
                    continue
                
                # Save content to file
                filename = f"buda_{building}_{domain}_{int(time.time())}.json"
                filepath = os.path.join(self.output_dir, building, domain, "raw", filename)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                
                print(f"💾 Saved {len(items)} items to {filepath}")
                
                # Create metadata entries
                for item in items:
                    metadata_entry = {
                        "filename": filename,
                        "nalanda_building": building,
                        "subject_domain": domain,
                        "path": f"dharmaganj/{building}/{domain}/raw/{filename}",
                        "lipi": "Devanagari",
                        "shakha": "BUDA",
                        "bhashya": "None"
                    }
                    metadata_updates.append(metadata_entry)
        
        # Update master catalog
        self._update_catalog(metadata_updates)
    
    def _update_catalog(self, new_entries: List[Dict]):
        """Update the master catalog with new entries"""
        try:
            with open(self.catalog_file, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            catalog = {"version": "1.0", "buildings": ["bagdevibhandar", "ratnodadhi", "ratnasagara", "ratnaranjaka"], "catalog": []}
        
        # Add new entries
        catalog['catalog'].extend(new_entries)
        
        # Save updated catalog
        with open(self.catalog_file, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Updated master catalog with {len(new_entries)} new entries")

def main():
    """Main execution function"""
    print("🚀 BUDA Data Fetcher for Vedic RAG AI")
    print("=" * 50)
    
    # Initialize fetcher
    fetcher = BudaDataFetcher()
    
    # Define search terms based on existing dharmaganj content
    # These terms are selected to complement existing Vedic/Buddhist collections
    search_terms = [
        # Core philosophical concepts
        "prajna", "upaya", "sunyata", "tathata", "bodhi",
        
        # Text types we want more of
        "sutra", "shastra", "tantra", "commentary", "bhashya",
        
        # Specific traditions/schools
        "madhyamaka", "yogacara", "vedanta", "sautrantika",
        
        # Technical terms
        "pramana", "nyaya", "dharma", "karma", "samsara",
        
        # Practices and concepts
        "meditation", "yoga", "mantra", "mandala", "bodhisattva"
    ]
    
    print(f"📝 Search terms: {', '.join(search_terms)}")
    print()
    
    # Search and categorize
    results = fetcher.search_and_categorize(search_terms)
    
    # Display summary
    print("\n📊 Results Summary:")
    for building, domains in results.items():
        total_items = sum(len(items) for items in domains.values())
        print(f"🏛️  {building}: {total_items} total items")
        for domain, items in domains.items():
            if items:
                print(f"   📁 {domain}: {len(items)} items")
    
    # Ask for confirmation before saving
    print(f"\n💾 Ready to save results to {fetcher.output_dir}")
    response = input("Save results? (y/N): ").strip().lower()
    
    if response == 'y':
        fetcher.save_results(results)
        print("✅ Results saved successfully!")
    else:
        print("❌ Results not saved.")

if __name__ == "__main__":
    main()
