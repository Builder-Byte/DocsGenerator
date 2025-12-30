# File Name

`summarize.py`

# Summary

# Summarize Code Documentation

## Table of Contents

1. [Overview](#overview)
2. [Architecture & Design](#architecture--design)
3. [Public Interfaces](#public-interfaces)
4. [Internal Logic](#internal-logic)
5. [Configuration & Environment](#configuration--environment)
6. [Usage Examples](#usage-examples)
7. [Edge Cases & Constraints](#edge-cases--constraints)
8. [Best Practices & Notes](#best-practices--notes)

## Overview

The `Summarize` class is the main entry point for generating AI summaries and Markdown documentation for all code files in a specified project folder. It reads all files, analyzes their code structure, generates AI summaries using an OpenRouter client, and creates both Markdown and JSON documentation.

## Architecture & Design

The `Summarize` class follows a simple yet effective architecture with the following key components:

- **DependencyGenerator**: Responsible for analyzing code files and extracting relevant information such as imports, functions, classes, etc.
- **OpenRouterClient**: Handles communication with the OpenRouter API to generate AI summaries of the code.
- **DocsCreator**: Converts the generated analysis and summary data into Markdown and JSON formats.

The class uses a shared processing status dictionary (`processing_status`) to update progress across multiple instances or users. It also employs a unique session ID for multi-user support and output folder isolation.

## Public Interfaces

### `Summarize`

**Signature**: `Summarize(folder_to_summarize: str, output_folder: str, session_id: Optional[str] = None, processing_status: Optional[Dict] = None, output_base_dir: Optional[str] = None)`

**Parameters**:

- `folder_to_summarize` (str): Path to the folder containing source code.
- `output_folder` (str): Name of the output folder for generated docs.
- `session_id` (Optional[str]): Optional unique session identifier for multi-user support.
- `processing_status` (Optional[Dict]): Optional reference to shared status dict for progress updates.
- `output_base_dir` (Optional[str]): Optional base directory for output files.

**Returns**: None

**Description**: Initializes the `Summarize` class and sets up the output folder structure.

### `summarize`

**Signature**: `summarize(self) -> None`

**Parameters**: None

**Returns**: None

**Description**: Processes all files in the project and generates documentation. It reads all project files, analyzes their code structure, generates AI summaries, and creates Markdown and JSON documentation.

### `_update_progress`

**Signature**: `_update_progress(self, current: int, total: int, current_file: str) -> None`

**Parameters**:

- `current` (int): Current file being processed.
- `total` (int): Total number of files in the project.
- `current_file` (str): Path to the current file being processed.

**Returns**: None

**Description**: Updates progress in the shared processing status dictionary.

## Internal Logic

The `summarize` method follows these critical workflows:

1. Reads all project files using the `FileExplorer` class.
2. Initializes the `OpenRouterClient`, `DependencyGenerator`, and `DocsCreator` instances.
3. Loops through each file, updating progress and performing the following steps:
   a. Generates code analysis using the `DependencyGenerator`.
   b. Generates an AI summary using the `OpenRouterClient` with retry logic.
   c. Creates safe filenames for output and generates documentation using the `DocsCreator`.

The `_update_progress` method updates the progress in the shared processing status dictionary, allowing for real-time progress tracking.

## Configuration & Environment

### Required environment variables

None

### Configuration options

- `folder_to_summarize`: Path to the folder containing source code.
- `output_folder`: Name of the output folder for generated docs.
- `session_id`: Optional unique session identifier for multi-user support.
- `processing_status`: Optional reference to shared status dict for progress updates.
- `output_base_dir`: Optional base directory for output files.

### External services or resources used

- OpenRouter API: Used to generate AI summaries of the code.

## Usage Examples

1. Initialize and run the `Summarize` class with a project folder and output folder:

```python
Summarize('mini_project', 'docs_output').summarize()
```

2. To use a custom session ID and output base directory:

```python
Summarize('mini_project', 'docs_output', session_id='my_session', output_base_dir='/path/to/output').summarize()
```

## Edge Cases & Constraints

### Limitations

- The `OpenRouterClient` might have rate limits or availability issues, which could affect the summary generation process.
- Large projects with many files might experience slower processing times or memory constraints.

### Assumptions

- The project folder contains only Python files.
- The `OpenRouterClient` is available and functioning correctly.

### Performance considerations

- Processing large projects might take considerable time, depending on the number of files and the OpenRouter API's response time.

## Best Practices & Notes

### Security considerations

- Ensure that the OpenRouter API key is kept secure and not exposed in the code or configuration.
- Be mindful of rate limits and API usage costs when using external services like OpenRouter.

### Maintainability tips

- Keep the `Summarize` class and its dependencies well-documented and organized for easy maintenance and updates.
- Regularly review and update the `ignore_folders` list in the `FileExplorer` initialization to exclude unnecessary folders from processing.

### Extension points

- The `Summarize` class can be extended to support additional file types or analysis tools by modifying the `DependencyGenerator` and `DocsCreator` classes.
- Custom progress tracking or reporting can be implemented by overriding or extending the `_update_progress` method.

## Imports

This script imports the following modules:

- `file_explorer_cli.FileExplorer`
  - **Available functions:** clear_file, write_to_files, write_to_json, write_to_md, readFiles, print_folder_not_found, getFiles, detect_language, get_manifest, __init__
  - **Source:** `file_explorer_cli.py`
- `dependency_generator.DependencyGenerator`
  - **Available functions:** _safe_parse, generateGraph, extract_imports, extract_functions, extract_classes, extract_docstrings, extract_type_hints, extract_top_level_constants, extract_todos, analyze_cross_library_imports, summarize_file, __init__, add_node
  - **Source:** `dependency_generator.py`
- `openrouter_client.OpenRouterClient`
  - **Available functions:** summarize, __init__
  - **Source:** `openrouter_client.py`
- `docs_creator.DocsCreator`
  - **Available functions:** __init__, ensure_output_directory, json_to_markdown
  - **Source:** `docs_creator.py`
- `time`
- `shutil`
- `os`
- `uuid`
- `typing.Dict`
- `typing.Optional`

## Functions

### `summarize()`

- **Arguments:** `self`
- **Returns:** `None`
- **Description:** Process all files in the project and generate documentation.

For each file:
1. Extract code structure (imports, functions, classes, etc.)
2. Perform cross-library analysis to link imports to source files
3. Generate AI summary of the code
4. Create Markdown and JSON documentation

### `_update_progress()`

- **Arguments:** `self, current, total, current_file`
- **Returns:** `None`
- **Description:** Update progress in the shared processing_status dict.

### `__init__()`

- **Arguments:** `self, folder_to_summarize, output_folder, session_id, processing_status, output_base_dir`
- **Returns:** `None`
- **Description:** Initialize the Summarize class.

Args:
    folder_to_summarize: Path to the folder containing source code
    output_folder: Name of the output folder for generated docs
    session_id: Optional unique session identifier for multi-user support
    processing_status: Optional reference to shared status dict for progress updates
    output_base_dir: Optional base directory for output files


## Classes

### `Summarize`

- **Methods:** `summarize, _update_progress, __init__`
- **Description:** Main class for summarizing code files in a project.

Reads all files from a folder, analyzes them using DependencyGenerator,
generates AI summaries, and creates Markdown documentation.


## Constants

No constants found.

---

*This documentation was generated automatically by DocsGenerator.*
