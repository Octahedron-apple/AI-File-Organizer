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

print(f"Found {len(files)} files.")
print(files)