import requests
import os

base_api = "https://api.github.com/repos/sanskritsahitya-com/data/contents"
raw_base = "https://raw.githubusercontent.com/sanskritsahitya-com/data/main"
dharmaganj_path = "dharmaganj"

response = requests.get(base_api)
if response.status_code == 200:
    contents = response.json()
    for item in contents:
        if item['type'] == 'dir' and item['name'] != 'code':
            folder = item['name']
            folder_path = os.path.join(dharmaganj_path, folder)
            os.makedirs(folder_path, exist_ok=True)
            # Get contents of folder
            folder_api = f"{base_api}/{folder}"
            folder_resp = requests.get(folder_api)
            if folder_resp.status_code == 200:
                folder_contents = folder_resp.json()
                for file_item in folder_contents:
                    if file_item['type'] == 'file':
                        file_name = file_item['name']
                        raw_url = f"{raw_base}/{folder}/{file_name}"
                        file_resp = requests.get(raw_url)
                        if file_resp.status_code == 200:
                            with open(os.path.join(folder_path, file_name), 'wb') as f:
                                f.write(file_resp.content)
                            print(f"Downloaded {folder}/{file_name}")
                        else:
                            print(f"Failed to download {raw_url}")
            else:
                print(f"Failed to get contents of {folder}")
else:
    print("Failed to get repo contents")
