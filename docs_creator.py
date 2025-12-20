import json
import os

class DocsCreator:

    def __init__(self):
        
        # Ensure the output directory exists
        self.ensure_output_directory("output/json/summary.md")

    def ensure_output_directory(self, output_file):
        """
        Ensure that the directory for the given output file exists.
        """
        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def json_to_markdown(self, json_input, output_file):
        self.ensure_output_directory(output_file)
        with open(output_file, 'w') as md_file:
            # Write the summary
            file_name = json_input.get("file_name", "No file name provided.")
            md_file.write("# File Name\n\n")
            md_file.write(f"{file_name}\n\n")
            
            summary = json_input.get("summary", "No summary provided.")
            md_file.write("# Summary\n\n")
            md_file.write(f"{summary}\n\n")

            # Write imports
            imports = json_input.get("imports", [])
            md_file.write("## Imports\n\n")
            if imports:
                md_file.write("This script imports the following modules:\n")
                for imp in imports:
                    md_file.write(f"- `{imp}`\n")
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

                    md_file.write(f"### {name}()\n\n")
                    md_file.write(f"- **Arguments:** {', '.join(args) if args else 'None'}\n")
                    md_file.write(f"- **Returns:** {returns}\n")
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
                    docstring = json_input.get("docstrings", {}).get("classes", {}).get(name, "No description provided.")

                    md_file.write(f"### {name}\n\n")
                    md_file.write(f"- **Description:** {docstring}\n\n")
            else:
                md_file.write("No classes found.\n")
            md_file.write("\n")

            # Write constants
            constants = json_input.get("constants", [])
            md_file.write("## Constants\n\n")
            if constants:
                md_file.write("This script defines the following constants:\n")
                for const in constants:
                    md_file.write(f"- `{const}`\n")
            else:
                md_file.write("No constants found.\n")
            md_file.write("\n")
