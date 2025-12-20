# Summarizer Prerequisite Projects

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


## Project Structure
```
├── dependency_generator.py
├── docs_creator.py
├── file_explorer_cli.py
├── gemini_client.py
├── main.py
├── openrouter_client.py
├── mini_project/
│   ├── main.py
│   ├── common/
│   │   ├── __init__.py
│   │   ├── logger.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   ├── parser.py
│   ├── dependency_generator/
│   │   ├── mini_project/
│   │   │   ├── output.txt
│   │   │   ├── read.txt
│   ├── utils/
│       ├── __init__.py
│       ├── helper.py
│       ├── math_ops.py
├── output/
│   ├── json/
│   ├── md/
│   ├── output.txt.txt
```

## Installation
1. Clone the repository:
   ```bash
   https://github.com/Builder-Byte/DocsGenerator```
2. Navigate to the project directory:
   ```bash
   cd DocsGenerator
   ```
3. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

## Usage
1. Run the main script:
   ```bash
   python main.py
   ```
2. Specify the folder to summarize in the `main.py` file.
3. Outputs will be generated in the `output` directory.


## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any inquiries, please contact [your email].
