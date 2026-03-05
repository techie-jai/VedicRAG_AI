# This script downloads the Itihasa dataset from CSV files and converts it into text files 
# formatted perfectly for Open WebUI's RAG system.

from huggingface_hub import hf_hub_download
import pandas as pd
import os

def main():
    print("Downloading Itihasa dataset CSV files from Huggingface...")
    
    # Suppress the symlink warning for Windows
    os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
    
    # Download the CSV files
    repo_id = "rahular/itihasa"
    
    try:
        print("Downloading train files...")
        train_en_path = hf_hub_download(repo_id=repo_id, filename="train.en.csv", repo_type="dataset")
        train_sn_path = hf_hub_download(repo_id=repo_id, filename="train.sn.csv", repo_type="dataset")
        
        print("Downloading validation files...")
        val_en_path = hf_hub_download(repo_id=repo_id, filename="dev.en.csv", repo_type="dataset")
        val_sn_path = hf_hub_download(repo_id=repo_id, filename="dev.sn.csv", repo_type="dataset")
        
        print("Downloading test files...")
        test_en_path = hf_hub_download(repo_id=repo_id, filename="test.en.csv", repo_type="dataset")
        test_sn_path = hf_hub_download(repo_id=repo_id, filename="test.sn.csv", repo_type="dataset")
        
        # Load the CSV files with error handling
        print("Loading CSV files...")
        
        def load_csv_safely(file_path, column_name):
            try:
                # Try standard CSV first
                df = pd.read_csv(file_path, header=None, names=[column_name])
                return df
            except:
                try:
                    # Try with different separator
                    df = pd.read_csv(file_path, header=None, names=[column_name], sep='\t')
                    return df
                except:
                    try:
                        # Try reading as plain text lines
                        with open(file_path, 'r', encoding='utf-8') as f:
                            lines = f.readlines()
                        data = [[line.strip()] for line in lines if line.strip()]
                        return pd.DataFrame(data, columns=[column_name])
                    except Exception as e:
                        print(f"Failed to load {file_path}: {e}")
                        return pd.DataFrame(columns=[column_name])
        
        train_en = load_csv_safely(train_en_path, 'en')
        train_sn = load_csv_safely(train_sn_path, 'sn')
        
        val_en = load_csv_safely(val_en_path, 'en')
        val_sn = load_csv_safely(val_sn_path, 'sn')
        
        test_en = load_csv_safely(test_en_path, 'en')
        test_sn = load_csv_safely(test_sn_path, 'sn')
        
        # Combine the data
        print("Combining data...")
        train_data = []
        for i in range(len(train_en)):
            train_data.append({
                'translation': {
                    'en': train_en.iloc[i]['en'],
                    'sn': train_sn.iloc[i]['sn']
                }
            })
        
        val_data = []
        for i in range(len(val_en)):
            val_data.append({
                'translation': {
                    'en': val_en.iloc[i]['en'],
                    'sn': val_sn.iloc[i]['sn']
                }
            })
        
        test_data = []
        for i in range(len(test_en)):
            test_data.append({
                'translation': {
                    'en': test_en.iloc[i]['en'],
                    'sn': test_sn.iloc[i]['sn']
                }
            })
        
        print(f"Loaded {len(train_data)} training, {len(val_data)} validation, {len(test_data)} test entries")
        
        # Create output directory
        output_dir = "itihasa_texts"
        os.makedirs(output_dir, exist_ok=True)
        
        # Combine all data and split into files
        all_data = train_data + val_data + test_data
        print(f"Total entries: {len(all_data)}")
        
        file_index = 1
        entry_count = 0
        max_entries_per_file = 20000  # Split into manageable chunks
        
        current_file = open(f"{output_dir}/itihasa_part_{file_index}.txt", "w", encoding="utf-8")
        
        print("Formatting and splitting data...")
        for item in all_data:
            en_text = item['translation']['en']
            sn_text = item['translation']['sn']
            
            # Format each entry clearly
            chunk = f"Sanskrit Shloka: {sn_text}\nEnglish Translation: {en_text}\n---\n"
            current_file.write(chunk)
            
            entry_count += 1
            if entry_count >= max_entries_per_file:
                current_file.close()
                file_index += 1
                current_file = open(f"{output_dir}/itihasa_part_{file_index}.txt", "w", encoding="utf-8")
                entry_count = 0
                print(f"Created file {file_index-1}, starting file {file_index}...")
        
        current_file.close()
        print(f"Success! Created {file_index} text files in the '{output_dir}' folder.")
        print(f"Total Sanskrit-English pairs processed: {len(all_data)}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to download the dataset. Please check your internet connection.")

if __name__ == "__main__":
    main()
