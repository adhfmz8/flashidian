from dotenv import load_dotenv
import os

from google import genai
from typing import List

import argparse

env = os.getenv("GOOGLE_API_KEY")

MAIN_PROMPT = """
You are a helpful assistant tasked with converting markdown notes into flashcards. Here’s what you need to do:

1. **Read and Understand**:
   - Analyze the content of the provided markdown notes.
   - Identify the key points, definitions, or concepts that can be transformed into flashcard-style questions and answers.

2. **Generate Flashcards**:
   - For each concept, create a question and answer pair.
   - Use concise language for both the question and answer to ensure clarity.

3. **Formatting Requirements**:
   - Output the flashcards in a tab-delimited format, with the question and answer separated by a single tab (`\t`).
   - Each flashcard should be on a new line.

4. **Markdown Content**:
Here are the notes (in markdown format) that you need to process:

"""


def load_api_key(env_path: str = None) -> str:
    """
    Function to get env variables and return google api key
    :param env_path: Path to the .env file
    :return: API key
    """
    load_dotenv(env_path)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found!")
    return api_key


def get_markdown_files(folder_path):
    """
    Gets all markdown files from folder path
    :param folder_path: the path to .md notes or obsidian folder
    :return: all markdown files as a str
    """

    if not os.path.isdir(folder_path):
        raise ValueError(f"The path {folder_path} is not a valid directory.")

    markdown_files = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(".md")
    ]

    if not markdown_files:
        raise ValueError(f"No markdown files found in the directory {folder_path}.")

    return markdown_files


def read_files_to_string(file_paths: List[str]):
    """
    Reads markdown files and outputs a concatentated string of them
    :param file_paths: list of .md files
    :return: string of concatenated md files
    """
    all_contents = []
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            all_contents.append(content)

    return "\n".join(all_contents)


def get_response(notes: str, key: str) -> str:
    """
    api call to get flashcards
    :param notes: parsed md notes as str
    :param key: google api key
    :return: formatted flashcards
    """
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp", contents=MAIN_PROMPT + notes
    )

    return response.text


def main():
    # Argument parsing
    parser = argparse.ArgumentParser(
        description="Convert markdown notes to tab-delimited flashcards using a Google API."
    )
    parser.add_argument(
        "folder", type=str, help="Path to the folder containing markdown files."
    )
    parser.add_argument(
        "--env",
        type=str,
        default=".env",
        help="Path to the .env file containing the GOOGLE_API_KEY (default: .env).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="flashcards.txt",
        help="Path to save the flashcards output (default: flashcards.txt in the current directory).",
    )
    args = parser.parse_args()

    try:
        # Load API key
        key = load_api_key(args.env)

        # Get markdown files and read contents
        files = get_markdown_files(args.folder)
        file_contents = read_files_to_string(files)

        # Generate flashcards via API
        response = get_response(file_contents, key)

        # Save output to file
        output_path = args.output
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write(response)

        print(f"Flashcards saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
