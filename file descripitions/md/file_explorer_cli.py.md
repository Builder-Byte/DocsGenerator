# File Name

file_explorer_cli.py

# Summary

**Summary:**

The provided Python script defines a `FileExplorer` class with methods to interact with files and folders. Here's a summary of its functionality:

1. **Initialization (`__init__`):**
   - Takes `root_dir` (default is current working directory), `output_file` (default is "output.txt"), and lists of `ignore_folders` and `ignore_files`.
   - Clears the output file upon initialization.

2. **File and Folder Operations:**
   - `clear_file(root_dir, output_file)`: Clears the specified output file in the given root directory.
   - `write_to_files(content, output_file)`: Appends the given content to the specified output file in the root directory.
   - `write_to_json(content, output_file)`: Writes the given content as JSON to the specified output file with a ".json" extension.
   - `write_to_md(content, output_file)`: Writes the given content as JSON to the specified output file with a ".md" extension.
   - `readFiles(output_file="read.txt")`: Reads all files in the root directory (excluding ignored files and folders), returns a dictionary with file names as keys and their contents as values.
   - `getFiles()`: Walks through the root directory, collects all non-ignored files, and writes their paths to the output file.

3. **Helper Methods:**
   - `print_folder_not_found(path)`: Prints an error message if the specified path (or root_dir if no path is given) is not a valid directory.
   - `detect_language(filename)`: Determines the programming language based on the file extension.
   - `get_manifest()`: Generates a manifest of files under the root directory with metadata (path, size, modification time, and detected language).

The `FileExplorer` class is designed to help explore, read, write, and manage files and folders in a specified root directory, while allowing for customization of ignored files and folders.

## Imports

This script imports the following modules:
- `os`
- `json`

## Functions

### clear_file()

- **Arguments:** self, root_dir, output_file
- **Returns:** None
- **Description:** None

### write_to_files()

- **Arguments:** self, content, output_file
- **Returns:** None
- **Description:** None

### write_to_json()

- **Arguments:** self, content, output_file
- **Returns:** None
- **Description:** None

### write_to_md()

- **Arguments:** self, content, output_file
- **Returns:** None
- **Description:** None

### readFiles()

- **Arguments:** self, output_file
- **Returns:** dict
- **Description:** None

### print_folder_not_found()

- **Arguments:** self, path
- **Returns:** bool
- **Description:** None

### getFiles()

- **Arguments:** self
- **Returns:** list
- **Description:** None

### detect_language()

- **Arguments:** self, filename
- **Returns:** str
- **Description:** None

### get_manifest()

- **Arguments:** self
- **Returns:** dict
- **Description:** Return a manifest of files under root_dir with metadata.

Manifest structure:
{
    "relative/path.py": {
        "path": "absolute/path",
        "size": 1234,
        "mtime": 1234567890.0,
        "language": "python"
    },
    ...
}

### __init__()

- **Arguments:** self, root_dir, output_file, ignore_folders, ignore_files
- **Returns:** None
- **Description:** None


## Classes

### FileExplorer

- **Description:** None


## Constants

No constants found.

