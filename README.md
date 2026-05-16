# AI File Organizer

This tool uses AI to categorize and organize files into folders.

## Setup

Install the dependency:
```
pip install ollama
```
Ensure Ollama is running with the qwen3.5:4b model.
```
ollama run qwen3.5:4b
```
## Usage

1. List categories in categories.txt (one per line).
2. Run the script:
```
python main.py
```
3. Enter the directory path when prompted.

The script creates a new folder with the organized files copied into category subfolders.