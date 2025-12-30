# File Name

`server.py`

# Summary

# **API Documentation**

## Table of Contents

1. [Overview](#overview)
2. [Architecture & Design](#architecture-design)
3. [Public Interfaces](#public-interfaces)
4. [Internal Logic](#internal-logic)
5. [Configuration & Environment](#configuration-environment)
6. [Usage Examples](#usage-examples)
7. [Edge Cases & Constraints](#edge-cases-constraints)
8. [Best Practices & Notes](#best-practices-notes)

## Overview

This FastAPI application provides a simple API for uploading ZIP files, extracting their contents, and running a summarization process on the extracted files in the background. It uses unique session IDs for multi-user isolation and tracks the processing status of each session.

## Architecture & Design

The application follows a simple, modular design with the following key components:

- **Main Application (`__init__.py`)**
  - Initializes the FastAPI application and configures CORS.
  - Sets up the directories for uploads, extracted files, and output.
  - Tracks the processing status of each session.

- **Summarizer Function (`summarizer`)**
  - Runs the summarization process in the background with session tracking.
  - Passes the processing status and output directory to the `Summarize` class for progress updates.

- **Zip Folder Function (`zip_folder`)**
  - Zips the output folder for a given session after the summarization process is completed.

- **Dependencies**
  - `fastapi`: FastAPI framework for building the API.
  - `summarize`: Custom module for summarization process (imported from `summarize.py`).

## Public Interfaces

### Endpoints

#### `GET /`

- **Purpose:** Check if the API is running.
- **Response:** A JSON response with the status "running".

#### `GET /download/{name}`

- **Purpose:** Download the generated ZIP file by name.
- **Parameters:**
  - `name` (str): The name of the ZIP file to download.
- **Response:** A `FileResponse` containing the requested ZIP file.
- **Exceptions:**
  - `404 Not Found`: Raised if the ZIP file is not found.

#### `GET /status/{session_id}`

- **Purpose:** Get the processing status for a given session.
- **Parameters:**
  - `session_id` (str): The session ID to retrieve the status for.
- **Response:** A JSON response containing the processing status for the given session ID.
- **Exceptions:**
  - `404 Not Found`: Raised if the session ID is not found.

#### `GET /sessions`

- **Purpose:** List all active processing sessions and their statuses.
- **Response:** A JSON response containing a list of active sessions and their total count.

#### `POST /upload`

- **Purpose:** Accept a ZIP file upload and extract its contents.
- **Request Body:**
  - `file` (UploadFile): The ZIP file to upload.
- **Response:** A JSON response containing the processing status, filename, session ID, and message.
- **Exceptions:**
  - `400 Bad Request`: Raised if the file is not a ZIP file or if the extracted folder is not found.

## Internal Logic

### Critical Algorithms or Workflows

1. **File Upload and Extraction:**
   - The application generates a unique session ID for each uploaded file.
   - It saves the uploaded file to a session-specific directory and extracts its contents to another session-specific directory.
   - The application looks for a nested folder with the same name as the uploaded ZIP file and uses it as the folder to be summarized if found.

2. **Summarization Process:**
   - The `summarizer` function runs the summarization process in the background using the `Summarize` class from the `summarize` module.
   - It passes the processing status and output directory to the `Summarize` class for progress updates.

3. **Zip Folder:**
   - The `zip_folder` function zips the output folder for a given session after the summarization process is completed.
   - It uses the session ID in the output path for multi-session isolation.

### Non-obvious Implementation Decisions

- The application uses unique session IDs for multi-user isolation to ensure that each user's uploads and processing are kept separate.
- It tracks the processing status of each session to provide real-time updates on the progress of the summarization process.

## Configuration & Environment

### Required Environment Variables

- None

### Configuration Options

- The `CORS` middleware allows all origins, credentials, methods, and headers for simplicity. In a production environment, you should configure specific origins, methods, and headers.
- The `BASE_DIR`, `UPLOAD_DIR`, `EXTRACT_DIR`, `OUTPUT_DIR`, and `OUTPUT_ZIP_DIR` variables define the directories used for storing uploaded files, extracted files, output files, and zipped output files, respectively.

### External Services or Resources Used

- None

## Usage Examples

### Upload a ZIP File and Start Summarization

```bash
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@path/to/your/file.zip" http://localhost:8000/upload
```

### Check the Processing Status of a Session

```bash
curl -X GET http://localhost:8000/status/<session_id>
```

### Download the Generated ZIP File

```bash
curl -X GET -o output.zip http://localhost:8000/download/<name>
```

### List All Active Processing Sessions

```bash
curl -X GET http://localhost:8000/sessions
```

## Edge Cases & Constraints

### Limitations

- The application assumes that the uploaded ZIP file contains a folder with the same name as the file (or a nested folder with the same name) that needs to be summarized.
- It does not support resuming interrupted summarization processes.

### Assumptions

- The application assumes that the `summarize` module provides a working summarization process.

### Performance Considerations

- The application runs the summarization process in the background using FastAPI's `BackgroundTasks` feature, which helps to keep the API responsive while long-running tasks are executed.
- However, the performance of the summarization process itself is dependent on the `summarize` module and may vary based on the size and complexity of the input data.

## Best Practices & Notes

### Security Considerations

- In a production environment, you should configure the `CORS` middleware to allow only specific origins, methods, and headers.
- You should also implement proper authentication and authorization mechanisms to protect the API and its resources.

### Maintainability Tips

- Keep the code modular and well-organized to make it easier to maintain and extend.
- Use meaningful variable and function names to improve code readability.
- Add comments and docstrings to explain the purpose and functionality of important code sections.

### Extension Points

- The application can be extended by adding new endpoints for different file types or processing tasks.
- You can also modify the `summarize` module to provide different summarization algorithms or improve the performance of the existing one.

## Style Guidelines

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use clear and concise variable, function, and endpoint names to improve code readability.
- Add docstrings to explain the purpose and functionality of important code sections, modules, and endpoints.
- Use Markdown formatting for documentation to make it easy to read and navigate.

## Imports

This script imports the following modules:

- `typing.Union`
- `os`
- `zipfile`
- `shutil`
- `uuid`
- `fastapi.FastAPI`
- `fastapi.File`
- `fastapi.UploadFile`
- `fastapi.HTTPException`
- `fastapi.BackgroundTasks`
- `fastapi.responses.FileResponse`
- `fastapi.responses.JSONResponse`
- `fastapi.middleware.cors.CORSMiddleware`
- `summarize.Summarize`
  - **Available functions:** summarize, _update_progress, __init__
  - **Source:** `summarize.py`

## Functions

### `summarizer()`

- **Arguments:** `folder_to_be_summarized, name, session_id`
- **Returns:** `None`
- **Description:** Run summarization in background with session tracking.

### `zip_folder()`

- **Arguments:** `name, session_id`
- **Returns:** `str`
- **Description:** Zip the output folder for a given session.

### `read_root()`

- **Arguments:** `None`
- **Returns:** `dict`
- **Description:** None


## Classes

No classes found.

## Type Hints

### `summarizer`

| Argument | Type |
|----------|------|
| `folder_to_be_summarized` | `str` |
| `name` | `str` |
| `session_id` | `str` |

**Returns:** `None`

### `zip_folder`

| Argument | Type |
|----------|------|
| `name` | `str` |
| `session_id` | `str` |

**Returns:** `str`

### `read_root`


**Returns:** `dict`

## Constants

No constants found.

---

*This documentation was generated automatically by DocsGenerator.*
