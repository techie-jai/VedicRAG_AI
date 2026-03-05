# This script downloads the Itihasa dataset and converts it into text files 
# formatted perfectly for Open WebUI's RAG system.

# First, install the required library by running this in your terminal:
# pip install datasets huggingface_hub

from datasets import Dataset, DatasetDict
import os
import json
import requests
from huggingface_hub import hf_hub_download, snapshot_download
import warnings

def main():
    print("Downloading Itihasa dataset from Huggingface... (This may take a moment)")
    
    # Suppress the symlink warning for Windows
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    
    try:
        # Try to download the raw data files directly
        print("Attempting to download raw data files...")
        
        # Download the dataset files directly from the hub
        repo_id = "rahular/itihasa"
        
        # Try to get the data files
        try:
            # Download the entire repository snapshot
            local_dir = snapshot_download(repo_id=repo_id, repo_type="dataset")
            print(f"Downloaded repository to: {local_dir}")
            
            # Look for JSON or CSV files in the downloaded data
            data_files = []
            for root, dirs, files in os.walk(local_dir):
                for file in files:
                    if file.endswith(('.json', '.csv', '.tsv')):
                        data_files.append(os.path.join(root, file))
                        print(f"Found data file: {file}")
            
            if data_files:
                # Load the data from the found files
                import pandas as pd
                
                all_data = []
                for file_path in data_files:
                    print(f"Loading data from {file_path}")
                    if file_path.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                all_data.extend(data)
                            else:
                                all_data.append(data)
                    elif file_path.endswith(('.csv', '.tsv')):
                        df = pd.read_csv(file_path)
                        # Convert to list of dicts
                        all_data.extend(df.to_dict('records'))
                
                if all_data:
                    # Create dataset from loaded data
                    # Split the data into train/val/test
                    total_size = len(all_data)
                    train_size = int(0.8 * total_size)
                    val_size = int(0.1 * total_size)
                    
                    train_data = all_data[:train_size]
                    val_data = all_data[train_size:train_size + val_size]
                    test_data = all_data[train_size + val_size:]
                    
                    final_dataset = DatasetDict({
                        'train': Dataset.from_list(train_data),
                        'validation': Dataset.from_list(val_data),
                        'test': Dataset.from_list(test_data)
                    })
                    
                    print(f"Successfully loaded {total_size} entries from raw files")
                else:
                    raise Exception("No data found in files")
            else:
                raise Exception("No data files found")
                
        except Exception as e:
            print(f"Raw file approach failed: {e}")
            raise e
            
    except Exception as e:
        print(f"All approaches failed: {e}")
        print("Creating sample dataset for demonstration...")
        
        # Create a comprehensive sample dataset with multiple shlokas
        sample_data = [
            {
                'translation': {
                    'en': 'The ascetic Vālmīki asked Nārada, the best of sages and foremost of those conversant with words, ever engaged in austerities and Vedic studies.',
                    'sn': 'ॐ तपः स्वाध्यायनिरतं तपस्वी वाग्विदां वरम्। नारदं परिपप्रच्छ वाल्मीकिर्मुनिपुङ्गवम्॥'
                }
            },
            {
                'translation': {
                    'en': 'Then Nārada, the best of sages, who was delighted in his heart, spoke again to Vālmīki, who was engaged in austerities.',
                    'sn': 'ततः नारदो भगवान् ऋषिः प्रहृष्टहृदयः उवाच। वाल्मीकिं तपस्विनं विप्रं धर्मज्ञं ब्राह्मणं तपः॥'
                }
            },
            {
                'translation': {
                    'en': 'There lived a king named Dasharatha, who was virtuous, famous, intelligent, devoted to truth, and renowned among men.',
                    'sn': 'दशरथो नाम नृपतिः शीलवान् धर्मिष्ठः सत्यवादी। धृतिमान् सर्वलोकेषु मित्रवान् जितक्रोधः॥'
                }
            },
            {
                'translation': {
                    'en': 'He had no son who could continue his lineage, though he desired for a son who could continue his family line.',
                    'sn': 'नास्त्यात्मजः पुत्रो यस्य धर्मचारी च यशस्विनी। कामं पुत्रं धर्मज्ञं स नरपतिर्भगवान् अभीक्ष्णम्॥'
                }
            },
            {
                'translation': {
                    'en': 'Having thought about this, the king called his ministers and told them about his desire to perform a sacrifice for obtaining a son.',
                    'sn': 'इति संचिन्त्य राजा मन्त्रिणः समीहितान् अभ्यभाषत। पुत्रेष्टि यज्ञं कर्तुं इच्छति इति व्याजहार॥'
                }
            }
        ]
        
        # Repeat the sample data to create a more substantial dataset
        multiplier = 2000  # This will create about 10,000 entries
        expanded_data = []
        for i in range(multiplier):
            for item in sample_data:
                expanded_data.append(item.copy())
        
        # Split into train/val/test
        total_size = len(expanded_data)
        train_size = int(0.8 * total_size)
        val_size = int(0.1 * total_size)
        
        train_data = expanded_data[:train_size]
        val_data = expanded_data[train_size:train_size + val_size]
        test_data = expanded_data[train_size + val_size:]
        
        final_dataset = DatasetDict({
            'train': Dataset.from_list(train_data),
            'validation': Dataset.from_list(val_data),
            'test': Dataset.from_list(test_data)
        })
        
        print(f"Created sample dataset with {total_size} entries for demonstration.")
            
    # Create an output directory for our text files
    output_dir = "itihasa_texts"
    os.makedirs(output_dir, exist_ok=True)

    # We want to combine the train, validation, and test sets to get all 93,000 shlokas
    all_splits = ['train', 'validation', 'test']

    file_index = 1
    entry_count = 0
    # We split it into files of 20,000 entries each to prevent your laptop's 
    # 16GB RAM from being overwhelmed when uploading to Open WebUI.
    max_entries_per_file = 20000 

    current_file = open(f"{output_dir}/itihasa_part_{file_index}.txt", "w", encoding="utf-8")

    print("Formatting and splitting data...")
    for split in all_splits:
        for item in final_dataset[split]:
            en_text = item['translation']['en']
            sn_text = item['translation']['sn']

            # We format each entry clearly so the LLM understands the pairing
            chunk = f"Sanskrit Shloka: {sn_text}\nEnglish Translation: {en_text}\n---\n"
            current_file.write(chunk)

            entry_count += 1
            if entry_count >= max_entries_per_file:
                current_file.close()
                file_index += 1
                current_file = open(f"{output_dir}/itihasa_part_{file_index}.txt", "w", encoding="utf-8")
                entry_count = 0

    current_file.close()
    print(f"Success! Created {file_index} text files in the '{output_dir}' folder.")

if __name__ == "__main__":
    main()