import ollama
import os
import subprocess
import json
from PIL import Image, ImageTk

def convert_to_png(input_path):
    try:
        img = Image.open(input_path)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        return None

path_input = input("Enter the directory path: ")
PATH = path_input.strip()

if os.path.isdir(PATH) == False:
    print("Error: path is not a valid directory.")
    exit(1)

f = open("categories.txt", "r")
lines = f.readlines()
f.close()

categories = []
for i in range(len(lines)):
    line = lines[i].strip()
    if len(line) > 0:
        categories.append(line)

ABS_PATH = os.path.abspath(os.path.normpath(PATH))
ORGANIZED_DIR = ABS_PATH + "-organized"

subprocess.run(["mkdir", "-p", ORGANIZED_DIR])

for i in range(len(categories)):
    category = categories[i]
    category_path = os.path.join(ORGANIZED_DIR, category)
    subprocess.run(["mkdir", "-p", category_path])

files_output = subprocess.check_output(["find", PATH, "-type", "f"], text=True)
files = files_output.splitlines()

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

IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".webp", ".gif"]

for i in range(len(files)):
    file_path = files[i]
    filename = os.path.basename(file_path)
    
    ext = os.path.splitext(filename)[1].lower()
    is_img = False
    for j in range(len(IMAGE_EXTS)):
        if ext == IMAGE_EXTS[j]:
            is_img = True
            break
            
    try:
        category_list_string = ""
        for j in range(len(categories)):
            category_list_string = category_list_string + categories[j]
            if j < len(categories) - 1:
                category_list_string = category_list_string + ", "

        images_param = None
        if is_img == True:
            images_param = [file_path]
            prompt = "You are given an image named: " + filename + ". Determine the best category for this file from the list of categories: " + category_list_string + ". Respond with a single tool call to 'organize_file'."
        else:
            content = subprocess.check_output(["cat", file_path], text=True, errors='ignore')
            if len(content) > 5000:
                content = content[0:5000]
            prompt = "You are given the name of the file: " + filename + " and its content: " + content + ". Determine the best category for the file from the list of categories: " + category_list_string + ". Respond with a single tool call to 'organize_file'."

        response = ollama.chat(
            model='qwen3.5:2b',
            messages=[
                {
                    'role': 'user', 
                    'content': prompt,
                    'images': images_param
                }
            ],
            tools=tools,
        )

        if 'tool_calls' in response['message']:
            tool_calls = response['message']['tool_calls']
            for k in range(len(tool_calls)):
                tool = tool_calls[k]
                if tool['function']['name'] == 'organize_file':
                    category = tool['function']['arguments']['category']
                    dest_dir = os.path.join(ORGANIZED_DIR, category)
                    subprocess.run(["cp", file_path, dest_dir], check=True)
                    print("File: " + filename + " -> Organized into '" + category + "' via tool call.")
        else:
            print("File: " + filename + " -> AI did not use the organization tool.")

    except Exception as e:
        print("Error processing " + filename + ": " + str(e))