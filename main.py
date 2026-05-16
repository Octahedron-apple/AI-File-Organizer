import ollama
import os
import subprocess
import json

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

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'organize_file',
            'description': 'Moves a file into a specific category folder based on its content or name.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'category': {
                        'type': 'string',
                        'description': 'The category to place the file in.',
                        'enum': categories,
                    },
                },
                'required': ['category'],
            },
        },
    }
]

for file_path in files:
    filename = os.path.basename(file_path)
    try:
        content = subprocess.check_output(["cat", file_path], text=True, errors='ignore')
        
        prompt = f"You are given the name of the file: {filename} and its content: {content}. Determine the best category for the file from the list of categories: {', '.join(categories)}. Respond with a single tool call to 'organize_file'."

        response = ollama.chat(
            model='qwen3.5:2b',
            messages=[
                {'role': 'user', 'content': prompt}
            ],
            tools=tools,
        )

        if 'tool_calls' in response['message']:
            for tool in response['message']['tool_calls']:
                if tool['function']['name'] == 'organize_file':
                    category = tool['function']['arguments']['category']
                    dest_dir = os.path.join(ORGANIZED_DIR, category)
                    subprocess.run(["cp", file_path, dest_dir], check=True)
                    print(f"File: {filename} -> Organized into '{category}' via tool call.")
        else:
            print(f"File: {filename} -> AI did not use the organization tool.")

    except Exception as e:
        print(f"Error processing {filename}: {e}")