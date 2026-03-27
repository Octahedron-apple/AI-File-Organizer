import ollama
import os
PATH=""
with open("categories.txt","r") as f:
    categories=f.readlines()

files = []

for root, dirs, a in os.walk(PATH):
    for i in a:
        files.append(os.path.join(root, i))
        print(len(files))
print(files)