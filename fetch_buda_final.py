#!/usr/bin/env python3
"""
Final attempt: Use working query templates and direct resource access
"""

import requests
import json
import time
import os
from typing import Dict, List, Optional

class BudaAPIClient:
    """Client for BUDA LDS-PDI API"""
    
    def __init__(self):
        self.base_url = "http://purl.bdrc.io"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Vedic-RAG-AI-Integration/1.0',
            'Accept': 'application/json'
        })
    
    def test_working_queries(self):
        """Test which query templates actually work"""
        try:
            response = self.session.get(f"{self.base_url}/queries")
            response.raise_for_status()
            queries = response.json()
            
            working_queries = []
            for query in queries[:10]:  # Test first 10
                query_id = query.get('id')
                try:
                    # Try simple parameters
                    params = {'pageSize': 5}
                    url = f"{self.base_url}/query/table/{query_id}"
                    test_response = self.session.get(url, params=params, timeout=10)
                    if test_response.status_code == 200:
                        working_queries.append(query_id)
                        print(f"✅ {query_id} works")
                    else:
                        print(f"❌ {query_id} failed: {test_response.status_code}")
                except Exception as e:
                    print(f"❌ {query_id} error: {str(e)[:50]}")
            
            return working_queries
        except Exception as e:
            print(f"Error testing queries: {e}")
            return []
    
    def get_works_by_type(self, work_type: str) -> Optional[Dict]:
        """Get works by type using idsByType query"""
        try:
            params = {
                'type': work_type,
                'pageSize': 50
            }
            
            url = f"{self.base_url}/query/table/idsByType"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting works of type '{work_type}': {e}")
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
    
    def get_all_persons(self) -> Optional[Dict]:
        """Get all persons to find Sanskrit authors"""
        try:
            params = {'pageSize': 100}
            url = f"{self.base_url}/query/table/Persons_all"
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting persons: {e}")
            return None

class DharmaganjCategorizer:
    """Categorizes BUDA content into dharmaganj structure"""
    
    CATEGORIES = {
        "ratnodadhi": {
            "shruti": ["veda", "rig", "sama", "yajur", "atharva", "samhita", "brahmana"],
            "sutra": ["sutra", "prajnaparamita", "guhyasamaja", "mahayana", "bodhicitta", "dharma"],
            "upanishad": ["upanishad", "upanisad", "brahmana", "aranyaka", "vedanta"]
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
    def categorize_text(title: str, content: str = "") -> tuple[str, str]:
        """Categorize a text based on title and content"""
        if not title:
            title = ""
        if not content:
            content = ""
            
        title_lower = title.lower()
        content_lower = content.lower()
        
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
                        domain_score += 3
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
            return "ratnaranjaka", "vividha"
        
        best_building = max(scores.keys(), key=lambda k: scores[k]['score'])
        return best_building, scores[best_building]['domain']

class BudaDataFetcher:
    """Main class for fetching and organizing BUDA data"""
    
    def __init__(self, output_dir: str = "dharmaganj"):
        self.client = BudaAPIClient()
        self.output_dir = output_dir
        self.catalog_file = os.path.join(output_dir, "bagdevibhandar", "master_catalog.json")
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
    
    def explore_buda_content(self) -> Dict:
        """Explore BUDA content using working query templates"""
        
        all_results = {
            'ratnodadhi': {'shruti': [], 'sutra': [], 'upanishad': []},
            'ratnasagara': {'cikitsavidya': [], 'nyaya_pramana': [], 'vyakarana': [], 
                          'jyotisha': [], 'arthashastra': []},
            'ratnaranjaka': {'itihasa': [], 'purana': [], 'kavya': [], 'vividha': []}
        }
        
        print("🔍 Testing which query templates work...")
        working_queries = self.client.test_working_queries()
        print(f"✅ Found {len(working_queries)} working queries: {working_queries}")
        
        # Try different approaches based on working queries
        
        # 1. Try to get works by different types
        work_types = ["Work", "Instance", "Person"]
        for work_type in work_types:
            print(f"\n📊 Getting works of type: {work_type}")
            results = self.client.get_works_by_type(work_type)
            
            if results and 'results' in results:
                print(f"✅ Found {len(results['results'])} items of type {work_type}")
                
                # Process first few items to see what we get
                for item in results['results'][:10]:  # Limit to first 10 for testing
                    resource_id = item.get('resource', '')
                    label = item.get('label', resource_id)
                    
                    # Get detailed info
                    resource_info = self.client.get_resource_info(resource_id)
                    if resource_info:
                        title = resource_info.get('title', label)
                        
                        # Categorize
                        building, domain = DharmaganjCategorizer.categorize_text(title)
                        
                        categorized_item = {
                            'resource_id': resource_id,
                            'title': title,
                            'content': str(item),  # Store the basic item info
                            'source': 'BUDA',
                            'work_type': work_type
                        }
                        
                        all_results[building][domain].append(categorized_item)
                        print(f"📚 {title[:50]}... -> {building}/{domain}")
                
                time.sleep(1)  # Rate limiting
        
        # 2. Try to get persons (might give us author information)
        print(f"\n👥 Getting persons...")
        persons = self.client.get_all_persons()
        if persons and 'results' in persons:
            print(f"✅ Found {len(persons['results'])} persons")
            
            # Look for Sanskrit-sounding names
            for person in persons['results'][:20]:
                name = person.get('label', '')
                if any(char in name.lower() for char in ['a', 'i', 'u', 'e', 'o']):  # Basic Sanskrit vowel check
                    resource_id = person.get('resource', '')
                    building, domain = "ratnaranjaka", "vividha"  # Default for persons
                    
                    categorized_item = {
                        'resource_id': resource_id,
                        'title': f"Person: {name}",
                        'content': str(person),
                        'source': 'BUDA',
                        'work_type': 'Person'
                    }
                    
                    all_results[building][domain].append(categorized_item)
                    print(f"👤 {name} -> {building}/{domain}")
        
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
        """Update master catalog with new entries"""
        try:
            with open(self.catalog_file, 'r', encoding='utf-8') as f:
                catalog = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            catalog = {"version": "1.0", "buildings": ["bagdevibhandar", "ratnodadhi", "ratnasagara", "ratnaranjaka"], "catalog": []}
        
        catalog['catalog'].extend(new_entries)
        
        with open(self.catalog_file, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Updated master catalog with {len(new_entries)} new entries")

def main():
    """Main execution function"""
    print("🚀 BUDA Content Explorer for Vedic RAG AI")
    print("=" * 50)
    
    fetcher = BudaDataFetcher()
    
    print("🔍 Exploring BUDA content structure...")
    results = fetcher.explore_buda_content()
    
    # Display summary
    print("\n📊 Results Summary:")
    for building, domains in results.items():
        total_items = sum(len(items) for items in domains.values())
        print(f"🏛️  {building}: {total_items} total items")
        for domain, items in domains.items():
            if items:
                print(f"   📁 {domain}: {len(items)} items")
    
    print(f"\n💾 Ready to save results to {fetcher.output_dir}")
    response = input("Save results? (y/N): ").strip().lower()
    
    if response == 'y':
        fetcher.save_results(results)
        print("✅ Results saved successfully!")
    else:
        print("❌ Results not saved.")

if __name__ == "__main__":
    main()
