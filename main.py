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

import gui
import tkinter as tk

IMAGE_EXTS = [".png", ".jpg", ".jpeg", ".webp", ".gif"]

gui_app = gui.OG()

current_index = 0

def process_next():
    global current_index
    if current_index >= len(files):
        gui_app.file_label.configure(text="Finished Organizing All Files!")
        return

    file_path = files[current_index]
    filename = os.path.basename(file_path)

    gui_app.file_label.configure(text="File Name: " + filename)
    gui_app.category_label.configure(text="Assigned Category: Processing...", fg="yellow")
    gui_app.response_text.delete("1.0", tk.END)
    gui_app.content_text.delete("1.0", tk.END)

    ext = os.path.splitext(filename)[1].lower()
    is_img = False
    for j in range(len(IMAGE_EXTS)):
        if ext == IMAGE_EXTS[j]:
            is_img = True
            break

    if is_img:
        gui_app.content_text.pack_forget()
        photo = convert_to_png(file_path)
        if photo is not None:
            gui_app.image_label.configure(image=photo)
            gui_app.image_label.image = photo
            gui_app.image_label.pack(expand=True, fill="both")
        else:
            gui_app.image_label.pack_forget()
    else:
        gui_app.image_label.pack_forget()
        gui_app.content_text.pack(expand=True, fill="both")
        try:
            content = subprocess.check_output(["cat", file_path], text=True, errors='ignore')
            if len(content) > 5000:
                content = content[0:5000]
            gui_app.content_text.insert("1.0", content)
        except Exception:
            gui_app.content_text.insert("1.0", "[Could not read file content]")

    try:
        category_list_string = ""
        for j in range(len(categories)):
            category_list_string = category_list_string + categories[j]
            if j < len(categories) - 1:
                category_list_string = category_list_string + ", "

        images_param = None
        if is_img:
            images_param = [file_path]
            prompt = "You are given an image named: " + filename + ". Determine the best category for this file from the list of categories: " + category_list_string + ". Respond with a single tool call to 'organize_file'."
        else:
            content = ""
            try:
                content = subprocess.check_output(["cat", file_path], text=True, errors='ignore')
                if len(content) > 5000:
                    content = content[0:5000]
            except Exception:
                pass
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
            stream=True
        )

        tool_calls = []
        for chunk in response:
            if 'message' in chunk:
                msg = chunk['message']
                if 'content' in msg and msg['content']:
                    text_chunk = msg['content']
                    gui_app.response_text.insert(tk.END, text_chunk)
                    print(text_chunk, end="", flush=True)
                    gui_app.root.update()
                if 'tool_calls' in msg and msg['tool_calls']:
                    for tc in msg['tool_calls']:
                        tool_calls.append(tc)
                        tool_desc = "\n[Tool Call: " + tc['function']['name'] + " with args: " + json.dumps(tc['function']['arguments']) + "]\n"
                        gui_app.response_text.insert(tk.END, tool_desc)
                        print(tool_desc, end="", flush=True)
                        gui_app.root.update()
        print("")

        assigned_category = "None"
        if len(tool_calls) > 0:
            for k in range(len(tool_calls)):
                tool = tool_calls[k]
                if tool['function']['name'] == 'organize_file':
                    category = tool['function']['arguments']['category']
                    assigned_category = category
                    dest_dir = os.path.join(ORGANIZED_DIR, category)
                    subprocess.run(["cp", file_path, dest_dir], check=True)
            
            gui_app.category_label.configure(text="Assigned Category: " + assigned_category, fg="green")
        else:
            gui_app.category_label.configure(text="Assigned Category: No tool call used", fg="red")

    except Exception as e:
        gui_app.category_label.configure(text="Error processing file", fg="red")
        gui_app.response_text.insert("1.0", str(e))

    current_index = current_index + 1
    gui_app.root.after(3000, process_next)

gui_app.root.after(100, process_next)
gui_app.root.mainloop()