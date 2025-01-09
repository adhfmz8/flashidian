# Markdown to Flashcards CLI

flashidian is a command-line tool that converts markdown notes into tab-delimited flashcards using the Google API. The flashcards are saved in a text file, ready to import into applications like Anki.

## Features
- Parses markdown notes from a specified folder.
- Extracts important concepts and generates question-answer flashcards.
- Outputs flashcards in a tab-delimited format.
- Saves the flashcards to a `.txt` file.

---

## Requirements
- Python 3.12 or higher
- Google API key
- Required Python packages:
  - `python-dotenv`
  - `google-genai` (or the appropriate library for the Google API)

---

## Installation

1. Clone this repository or download `script.py`:
2. Download required packages with UV
3. Set up your .env file to store the Google API key:

## Usage
Run the script using the following syntax:

`uv run script.py <folder_path> [--env <path_to_env>] [--output <output_file>]`

### Arguments
- folder (required): Path to the folder containing markdown files to process
- --env (optional): Path to the .env file containing the Google API key. Defaults to .env in the current directory.
- --output (optional): Path to save the generated flashcards file. Defaults to flashcards.txt in the current directory.
