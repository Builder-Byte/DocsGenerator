# File Name

docs_generator.py

# Summary

**Summary of the provided Python script:**

The script generates documentation for a project based on a given manifest file. Here's a breakdown of its functionality:

1. **Import Statements:**
   - `json`, `os`, `pathlib`, `typing`
   - `DependencyGenerator` and `OpenRouterClient` (assumed to be defined elsewhere)

2. **Functions:**

   - **`build_import_graph(manifest: Dict[str, Dict]) -> Dict[str, list]`:**
     - Constructs an import graph for the project by extracting imports from each file using `DependencyGenerator`.

   - **`generate_module_docs(manifest: Dict[str, Dict], out_dir: Path, client: OpenRouterClient)`:**
     - Generates module-level documentation for each file in the project.
     - Summarizes the content of each file using an LLM (with a heuristic fallback) and extracts AST metadata using `DependencyGenerator`.
     - Writes the generated documentation to Markdown files in the specified output directory.

   - **`generate_project_readme(summaries: Dict[str, str], out_dir: Path, client: OpenRouterClient)`:**
     - Generates a project-level README by combining file summaries and using an LLM to create a concise project description.

   - **`generate_docs(manifest_path: str = 'output/manifest.json', out_dir: str = 'output/docs')`:**
     - The main function that loads the manifest, initializes an `OpenRouterClient`, and calls the above functions to generate module docs, a project README, and an import graph JSON file.

3. **Main Script Execution:**
   - The script is run as a standalone script (`if __name__ == '__main__':`), triggering the `generate_docs()` function with default manifest and output directory paths.

In essence, this script automates the generation of project documentation, including module-level docs, a project README, and an import graph, based on a given manifest file and an OpenRouterClient for summarization tasks.

## Imports

This script imports the following modules:
- `json`
- `os`
- `pathlib.Path`
- `typing.Dict`
- `dependency_generator.DependencyGenerator`
- `openrouter_client.OpenRouterClient`

## Functions

### build_import_graph()

- **Arguments:** manifest
- **Returns:** Dict[str, list]
- **Description:** None

### generate_module_docs()

- **Arguments:** manifest, out_dir, client
- **Returns:** None
- **Description:** None

### generate_project_readme()

- **Arguments:** summaries, out_dir, client
- **Returns:** None
- **Description:** None

### generate_docs()

- **Arguments:** manifest_path, out_dir
- **Returns:** None
- **Description:** None


## Classes

No classes found.

## Constants

No constants found.

