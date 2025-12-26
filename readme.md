# DocsGenerator

## Overview
This repository contains a collection of Python scripts and modules designed to summarize and analyze code files. The project leverages tools like AST parsing, dependency generation, and integration with OpenAI's API for summarization.

## Features
- **File Explorer**: Reads and organizes files from a specified directory.
- **Dependency Generator**: Extracts imports, functions, classes, and other metadata from Python scripts.
- **OpenRouter Client**: Integrates with OpenAI's API for code summarization.
- **Docs Creator**: Converts JSON metadata into Markdown documentation.

## Technologies Used

- **Abstract Syntax Tree (AST)**: Utilized for parsing Python scripts to extract imports, functions, classes, and other metadata.
- **Multi-file Parsing**: Supports analyzing multiple files within a directory structure to generate comprehensive summaries.
- **OpenAI API Integration**: Leverages OpenAI's language models for generating human-readable summaries of code files.
- **Markdown Generation**: Converts extracted metadata into well-structured Markdown documentation.
- **File System Operations**: Includes utilities for reading, writing, and organizing files efficiently.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Builder-Byte/DocsGenerator
   ```
2. Navigate to the project directory:
   ```bash
   cd DocsGenerator/backend
   ```
3. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install the requirements:
   ```bash
   pip install -r requirement.txt
   ```
5. Navigate to frontend:
   ``` bash
   cd ../frontend
   ```
6. Install the dependency:
   ``` bash
   npm install
   ```


## Usage
#### For CLI usage:

1. Specify the folder to summarize in the `summarize.py` file.
2. Run the main script for cli usage:
   ```bash
   python summarize.py
   ```
   manually define the folder names inside first
3. Outputs will be generated in the `output` directory.

#### For Server usage:
1. Run the backend server:
   ```bash
   fastapi dev backend/server.py
   ```
2. Run the frontend server:
   ``` bash
   npm run dev
   ```   

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
