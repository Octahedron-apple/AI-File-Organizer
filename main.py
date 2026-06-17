import ollama
import os
import subprocess
import json
from PIL import Image, ImageTk

def convert_to_png(input_path):
    try:
        import customtkinter as ctk
        img = Image.open(input_path)
        img.thumbnail((400, 400))
        return ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
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
    gui_app.category_label.configure(text="Assigned Category: Processing...", text_color="yellow")
    gui_app.response_text.delete("0.0", "end")
    gui_app.content_text.delete("0.0", "end")
    
    if len(files) > 0:
        gui_app.progress_bar.set(current_index / len(files))

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
            gui_app.content_text.insert("0.0", content)
        except Exception:
            gui_app.content_text.insert("0.0", "[Could not read file content]")

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

        provider = gui_app.provider_var.get()
        model = gui_app.model_var.get()
        api_key = gui_app.api_key_var.get()

        tool_calls = []

        if provider == "Ollama":
            response = ollama.chat(
                model=model,
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

            for chunk in response:
                if 'message' in chunk:
                    msg = chunk['message']
                    if 'content' in msg and msg['content']:
                        text_chunk = msg['content']
                        gui_app.response_text.insert("end", text_chunk)
                        print(text_chunk, end="", flush=True)
                        gui_app.root.update()
                    if 'tool_calls' in msg and msg['tool_calls']:
                        for tc in msg['tool_calls']:
                            tool_calls.append(tc)
                            tool_desc = "\n[Tool Call: " + tc['function']['name'] + " with args: " + json.dumps(tc['function']['arguments']) + "]\n"
                            gui_app.response_text.insert("end", tool_desc)
                            print(tool_desc, end="", flush=True)
                            gui_app.root.update()
            print("")
        else: # OpenRouter
            import openai
            client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
            )
            
            content_list = []
            if is_img:
                import base64
                with open(file_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    ext = os.path.splitext(file_path)[1].lower()
                    mime_type = "image/jpeg"
                    if ext == ".png": mime_type = "image/png"
                    elif ext == ".webp": mime_type = "image/webp"
                    elif ext == ".gif": mime_type = "image/gif"
                content_list.append({"type": "text", "text": prompt})
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{mime_type};base64,{base64_image}"}
                })
            else:
                content_list.append({"type": "text", "text": prompt})
                
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content_list}],
                tools=tools,
                stream=False
            )
            
            msg = response.choices[0].message
            if msg.content:
                text_chunk = msg.content
                gui_app.response_text.insert("end", text_chunk)
                print(text_chunk)
                gui_app.root.update()
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    args_dict = json.loads(tc.function.arguments)
                    tool_calls.append({
                        "function": {
                            "name": tc.function.name,
                            "arguments": args_dict
                        }
                    })
                    tool_desc = "\n[Tool Call: " + tc.function.name + " with args: " + tc.function.arguments + "]\n"
                    gui_app.response_text.insert("end", tool_desc)
                    print(tool_desc)
                    gui_app.root.update()


        assigned_category = "None"
        if len(tool_calls) > 0:
            for k in range(len(tool_calls)):
                tool = tool_calls[k]
                if tool['function']['name'] == 'organize_file':
                    category = tool['function']['arguments']['category']
                    assigned_category = category
                    dest_dir = os.path.join(ORGANIZED_DIR, category)
                    subprocess.run(["cp", file_path, dest_dir], check=True)
            
            gui_app.category_label.configure(text="Assigned Category: " + assigned_category, text_color="#2ECC71")
        else:
            gui_app.category_label.configure(text="Assigned Category: No tool call used", text_color="#E74C3C")

    except Exception as e:
        gui_app.category_label.configure(text="Error processing file", text_color="#E74C3C")
        gui_app.response_text.insert("0.0", str(e))

    current_index = current_index + 1
    gui_app.root.after(3000, process_next)

def start_organizing():
    gui_app.start_button.configure(state="disabled")
    process_next()

gui_app.start_button.configure(command=start_organizing)
gui_app.root.mainloop()