import json
import os
from typing import Dict, List, Any, Optional


class DocsCreator:
    """Creates documentation in Markdown format from parsed code analysis."""

    def __init__(self) -> None:
        """Initialize the DocsCreator."""
        # Ensure the output directory exists
        self.ensure_output_directory("output/json/summary.md")

    def ensure_output_directory(self, output_file: str) -> None:
        """
        Ensure that the directory for the given output file exists.
        
        Args:
            output_file: Path to the output file
        """
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def json_to_markdown(self, json_input: Dict[str, Any], output_file: str) -> None:
        """
        Convert JSON analysis data to a Markdown documentation file.
        
        Args:
            json_input: Dictionary containing parsed code analysis
            output_file: Path to write the Markdown file
        """
        self.ensure_output_directory(output_file)
        with open(output_file, 'w', encoding='utf-8') as md_file:
            # Write the summary
            file_name = json_input.get("file_name", "No file name provided.")
            md_file.write("# File Name\n\n")
            md_file.write(f"`{file_name}`\n\n")
            
            summary = json_input.get("summary", "No summary provided.")
            md_file.write("# Summary\n\n")
            md_file.write(f"{summary}\n\n")

            # Write imports with cross-library analysis
            imports = json_input.get("imports", [])
            cross_library_info = json_input.get("cross_library_functions", {})
            md_file.write("## Imports\n\n")
            if imports:
                md_file.write("This script imports the following modules:\n\n")
                for imp in imports:
                    md_file.write(f"- `{imp}`\n")
                    # Add cross-library function details if available
                    if imp in cross_library_info:
                        func_info = cross_library_info[imp]
                        if func_info.get("functions"):
                            md_file.write(f"  - **Available functions:** {', '.join(func_info['functions'])}\n")
                        if func_info.get("source_file"):
                            md_file.write(f"  - **Source:** `{func_info['source_file']}`\n")
            else:
                md_file.write("No imports found.\n")
            md_file.write("\n")

            # Write functions
            functions = json_input.get("functions", [])
            md_file.write("## Functions\n\n")
            if functions:
                for func in functions:
                    name = func.get("name", "Unnamed function")
                    args = func.get("args", [])
                    returns = func.get("returns", "No return value specified")
                    docstring = json_input.get("docstrings", {}).get("functions", {}).get(name, "No description provided.")

                    md_file.write(f"### `{name}()`\n\n")
                    md_file.write(f"- **Arguments:** `{', '.join(args) if args else 'None'}`\n")
                    md_file.write(f"- **Returns:** `{returns}`\n")
                    md_file.write(f"- **Description:** {docstring}\n\n")
            else:
                md_file.write("No functions found.\n")
            md_file.write("\n")

            # Write classes
            classes = json_input.get("classes", [])
            md_file.write("## Classes\n\n")
            if classes:
                for cls in classes:
                    name = cls.get("name", "Unnamed class")
                    bases = cls.get("bases", [])
                    methods = cls.get("methods", [])
                    docstring = json_input.get("docstrings", {}).get("classes", {}).get(name, "No description provided.")

                    md_file.write(f"### `{name}`\n\n")
                    if bases:
                        md_file.write(f"- **Inherits from:** `{', '.join(bases)}`\n")
                    if methods:
                        md_file.write(f"- **Methods:** `{', '.join(methods)}`\n")
                    md_file.write(f"- **Description:** {docstring}\n\n")
            else:
                md_file.write("No classes found.\n")
            md_file.write("\n")

            # Write type hints
            type_hints = json_input.get("type_hints", {})
            if type_hints:
                md_file.write("## Type Hints\n\n")
                for func_name, hints in type_hints.items():
                    md_file.write(f"### `{func_name}`\n\n")
                    args = hints.get("args", {})
                    if args:
                        md_file.write("| Argument | Type |\n")
                        md_file.write("|----------|------|\n")
                        for arg, hint in args.items():
                            md_file.write(f"| `{arg}` | `{hint or 'Any'}` |\n")
                    returns = hints.get("returns")
                    if returns:
                        md_file.write(f"\n**Returns:** `{returns}`\n\n")

            # Write constants
            constants = json_input.get("constants", [])
            md_file.write("## Constants\n\n")
            if constants:
                md_file.write("This script defines the following constants:\n\n")
                md_file.write("| Name | Value |\n")
                md_file.write("|------|-------|\n")
                for const in constants:
                    if isinstance(const, dict):
                        md_file.write(f"| `{const.get('name', 'Unknown')}` | `{const.get('value', 'N/A')}` |\n")
                    else:
                        md_file.write(f"| `{const}` | - |\n")
            else:
                md_file.write("No constants found.\n")
            md_file.write("\n")
            
            md_file.write("---\n\n")
            md_file.write("*This documentation was generated automatically by DocsGenerator.*\n")
