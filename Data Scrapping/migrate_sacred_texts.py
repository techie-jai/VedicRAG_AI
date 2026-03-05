import os
import shutil
import json
from pathlib import Path

# Mapping of sacred texts categories to dharmaganj folders
MIGRATION_MAP = {
    # Vedas -> ratnodadhi/shruti (Vedas are part of Shruti)
    "Vedas": {
        "target": "dharmaganj/ratnodadhi/shruti",
        "description": "Vedic texts (Rig, Sama, Yajur, Atharva Vedas)"
    },
    
    # Upanishads -> ratnodadhi/upanishad
    "Upanishads": {
        "target": "dharmaganj/ratnodadhi/upanishad",
        "description": "Upanishadic philosophical texts"
    },
    
    # Bhagavad Gita -> ratnodadhi/srimadbhagavadgita
    "Bhagavad Gita": {
        "target": "dharmaganj/ratnodadhi/srimadbhagavadgita",
        "description": "Bhagavad Gita translations"
    },
    
    # Puranas -> ratnodadhi/purana (create if needed)
    "Puranas": {
        "target": "dharmaganj/ratnodadhi/purana",
        "description": "Puranic texts"
    },
    
    # Epics (Mahabharata & Ramayana) -> ratnaranjaka
    "Epics": {
        "target": "dharmaganj/ratnaranjaka/itihasa",
        "description": "Epic texts (Mahabharata, Ramayana)"
    },
    
    # Vedanta -> ratnasagara/vedanta (create if needed)
    "Vedanta": {
        "target": "dharmaganj/ratnasagara/vedanta",
        "description": "Vedantic philosophical texts"
    },
    
    # Primary Texts (Dharmaśāstra, Brahmana, Sutras) -> ratnodadhi/sutra
    "Primary Texts": {
        "target": "dharmaganj/ratnodadhi/sutra",
        "description": "Dharmaśāstra, Brahmana, and Sutra texts"
    },
    
    # Later Texts (Yoga, Classical) -> ratnasagara/yoga (create if needed)
    "Later Texts": {
        "target": "dharmaganj/ratnasagara/yoga",
        "description": "Later philosophical and yogic texts"
    },
    
    # Modern Books -> ratnaranjaka/vividha (miscellaneous)
    "Modern Books": {
        "target": "dharmaganj/ratnaranjaka/vividha",
        "description": "Modern and contemporary texts"
    }
}

def migrate_sacred_texts():
    """Migrate sacred texts from sacred_texts_hindu to dharmaganj"""
    
    source_dir = "sacred_texts_hindu"
    migration_log = {
        "total_files": 0,
        "migrated": 0,
        "failed": 0,
        "details": {}
    }
    
    print("=" * 70)
    print("SACRED TEXTS MIGRATION TO DHARMAGANJ")
    print("=" * 70)
    
    for category, mapping in MIGRATION_MAP.items():
        source_path = os.path.join(source_dir, category)
        target_path = mapping["target"]
        
        if not os.path.exists(source_path):
            print(f"\n⚠️  Source directory not found: {source_path}")
            continue
        
        # Create target directory if it doesn't exist
        os.makedirs(target_path, exist_ok=True)
        
        print(f"\n{'─' * 70}")
        print(f"📂 Category: {category}")
        print(f"   Description: {mapping['description']}")
        print(f"   Source: {source_path}")
        print(f"   Target: {target_path}")
        print(f"{'─' * 70}")
        
        category_log = {
            "source": source_path,
            "target": target_path,
            "files": []
        }
        
        # Get all text files in the category
        text_files = [f for f in os.listdir(source_path) if f.endswith('.txt')]
        
        print(f"Found {len(text_files)} files to migrate")
        
        for filename in text_files:
            source_file = os.path.join(source_path, filename)
            target_file = os.path.join(target_path, filename)
            
            try:
                # Copy file to target location
                shutil.copy2(source_file, target_file)
                print(f"  ✓ {filename}")
                
                category_log["files"].append({
                    "filename": filename,
                    "status": "migrated",
                    "size": os.path.getsize(target_file)
                })
                
                migration_log["migrated"] += 1
                
            except Exception as e:
                print(f"  ✗ {filename} - Error: {str(e)[:50]}")
                category_log["files"].append({
                    "filename": filename,
                    "status": "failed",
                    "error": str(e)[:100]
                })
                migration_log["failed"] += 1
            
            migration_log["total_files"] += 1
        
        migration_log["details"][category] = category_log
    
    # Save migration log
    log_path = "dharmaganj/migration_log_sacred_texts.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(migration_log, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"Total files processed: {migration_log['total_files']}")
    print(f"Successfully migrated: {migration_log['migrated']}")
    print(f"Failed: {migration_log['failed']}")
    print(f"Success rate: {(migration_log['migrated'] / migration_log['total_files'] * 100):.1f}%")
    print(f"\nMigration log saved to: {log_path}")
    print("=" * 70)
    
    return migration_log

def verify_migration():
    """Verify that files were migrated correctly"""
    print("\n" + "=" * 70)
    print("VERIFICATION: Checking dharmaganj structure")
    print("=" * 70)
    
    for category, mapping in MIGRATION_MAP.items():
        target_path = mapping["target"]
        
        if os.path.exists(target_path):
            files = [f for f in os.listdir(target_path) if f.endswith('.txt')]
            total_size = sum(os.path.getsize(os.path.join(target_path, f)) for f in files)
            print(f"\n✓ {category}")
            print(f"  Location: {target_path}")
            print(f"  Files: {len(files)}")
            print(f"  Total size: {total_size / (1024*1024):.2f} MB")
        else:
            print(f"\n✗ {category} - Directory not found: {target_path}")

if __name__ == "__main__":
    print("\n🔄 Starting migration of sacred texts to dharmaganj...\n")
    
    # Run migration
    migration_log = migrate_sacred_texts()
    
    # Verify migration
    verify_migration()
    
    print("\n✅ Migration complete!")
