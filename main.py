import ollama
import os

PATH = input("Enter the directory path: ").strip()

if not os.path.isdir(PATH):
    print(f"Error: {PATH} is not a valid directory.")
    exit(1)

with open("categories.txt", "r") as f:
    categories = f.readlines()

files = []

for root, dirs, filenames in os.walk(PATH):
    for filename in filenames:
        files.append(os.path.join(root, filename))

for file_path in files:
    filename = os.path.basename(file_path)
    prompt = f"Categorize the file '{filename}' into one of these categories: {', '.join([c.strip() for c in categories])}. Respond with only the category name."
    
    try:
        response = ollama.chat(model='qwen3.5:4b', messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
        category = response['message']['content'].strip()
        print(f"File: {filename} -> Category: {category}")
    except Exception as e:
        print(f"Error categorizing {filename}: {e}")