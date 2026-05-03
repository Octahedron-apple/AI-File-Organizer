import ollama
import os
import subprocess

PATH = input("Enter the directory path: ").strip()

if not os.path.isdir(PATH):
    print(f"Error: {PATH} is not a valid directory.")
    exit(1)

with open("categories.txt", "r") as f:
    categories = [line.strip() for line in f.readlines() if line.strip()]

ABS_PATH = os.path.abspath(os.path.normpath(PATH))
ORGANIZED_DIR = ABS_PATH + "-organized"
if not os.path.exists(ORGANIZED_DIR):
    os.makedirs(ORGANIZED_DIR)
for category in categories:
    category_path = os.path.join(ORGANIZED_DIR, category)
    if not os.path.exists(category_path):
        os.makedirs(category_path)
files = []

for root, dirs, filenames in os.walk(PATH):
    for filename in filenames:
        files.append(os.path.join(root, filename))

for file_path in files:
    filename = os.path.basename(file_path)
    prompt = f"Categorize the file '{filename}' into one of these categories: {', '.join(categories)}. Respond with only the category name."
    try:
        response = ollama.chat(model='qwen3.5:4b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        category = response['message']['content'].strip()
        
        if category in categories:
            dest_dir = os.path.join(ORGANIZED_DIR, category)
            subprocess.run(["cp", file_path, dest_dir], check=True)
            print(f"File: {filename} -> Categorized as '{category}' and copied.")
        else:
            print(f"File: {filename} -> Unknown category returned: '{category}'")
            
    except Exception as e:
        print(f"Error processing {filename}: {e}")