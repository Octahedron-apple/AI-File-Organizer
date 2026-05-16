# AI File Organizer

This tool uses AI to categorize and organize files based on their names and full content.

## Setup

Install the dependency:
```
pip install ollama
```

Ensure Ollama is running with the qwen3.5:2b model:
```
ollama run qwen3.5:2b
```

## Usage

1. List your desired categories in categories.txt (one per line).
2. Run the script:
```
python main.py
```
3. Provide the full path to the directory you want to organize.

## How it works

The script traverses your files and reads their entire content. It provides this information to the qwen3.5:2b model, which then uses a function call to determine the best category. A new directory ending in -organized is created where all files are sorted into their respective subfolders.