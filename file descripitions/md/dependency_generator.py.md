# File Name

dependency_generator.py

# Summary

**Summary of the Python Source Code File:**

1. **File Description:** The file contains a Python class named `DependencyGenerator` that uses the Abstract Syntax Tree (AST) to extract and analyze various aspects of Python code, such as imports, functions, classes, docstrings, type hints, and top-level constants.

2. **Imported Libraries:**
   - `json` and `ast` (built-in)
   - `graphviz` (if available)

3. **Class: DependencyGenerator**
   - **Methods:**
     - `_safe_parse(content)`: Safely parses the given Python code content using `ast.parse()` and returns the resulting AST or `None` if parsing fails.
     - `generateGraph(content)`: Generates a graph using `graphviz` to visualize the AST of the given Python code content. Skips graph generation if `graphviz` is not available.
     - `extract_imports(content)`: Extracts import statements from the given Python code content and returns a list of imported modules or module aliases.
     - `extract_functions(content)`: Extracts function definitions from the given Python code content and returns a list of dictionaries, where each dictionary represents a function with its name, arguments, return type, and docstring.
     - `extract_classes(content)`: Extracts class definitions from the given Python code content and returns a list of dictionaries, where each dictionary represents a class with its name, bases, methods, and docstring.
     - `extract_docstrings(content)`: Extracts the module-level docstring and per-symbol (functions and classes) docstrings from the given Python code content.
     - `extract_type_hints(content)`: Extracts simple type hints from top-level functions in the given Python code content and returns a dictionary mapping function names to their argument and return type hints.
     - `extract_top_level_constants(content)`: Extracts module-level simple constants (NAME = Constant) from the given Python code content and returns a list of dictionaries, where each dictionary represents a constant with its name and value.
     - `extract_todos(content)`: Extracts TODO and FIXME comments from the given Python code content along with their line numbers.
     - `summarize_file(content)`: Returns a combined summary dictionary for the given Python code content using the various extractor methods.
     - `__init__()`: The constructor method for the `DependencyGenerator` class.

4. **Usage:** The `DependencyGenerator` class can be used to analyze and extract various aspects of Python code, which can be useful for code analysis, documentation generation, or dependency management.

## Imports

This script imports the following modules:
- `json`
- `ast`
- `graphviz.Digraph`

## Functions

### _safe_parse()

- **Arguments:** self, content
- **Returns:** None
- **Description:** None

### generateGraph()

- **Arguments:** self, content
- **Returns:** None
- **Description:** None

### extract_imports()

- **Arguments:** self, content
- **Returns:** list
- **Description:** None

### extract_functions()

- **Arguments:** self, content
- **Returns:** list
- **Description:** None

### extract_classes()

- **Arguments:** self, content
- **Returns:** list
- **Description:** Return classes with bases, methods and docstring.

Returns list of dicts: {name, bases, methods, docstring}

### extract_docstrings()

- **Arguments:** self, content
- **Returns:** dict
- **Description:** Return module docstring and per-symbol docstrings.

### extract_type_hints()

- **Arguments:** self, content
- **Returns:** None
- **Description:** Extract simple type hints from top-level functions.

Returns dict mapping function name to {'args': {arg: annotation}, 'returns': annotation}

### extract_top_level_constants()

- **Arguments:** self, content
- **Returns:** None
- **Description:** Return module-level simple constants (NAME = Constant).

Returns list of dicts: {name, value_repr}

### extract_todos()

- **Arguments:** self, content
- **Returns:** None
- **Description:** Return list of comment TODO/FIXME lines with line numbers.

### summarize_file()

- **Arguments:** self, content
- **Returns:** None
- **Description:** Return a combined summary dict for a file using the various extractors.

### __init__()

- **Arguments:** self
- **Returns:** None
- **Description:** None

### add_node()

- **Arguments:** node, parent
- **Returns:** None
- **Description:** None


## Classes

### DependencyGenerator

- **Description:** None


## Constants

No constants found.

