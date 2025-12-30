import os
import json
from typing import Dict, List, Optional, Set


class FileExplorer:
    """File system explorer for reading and organizing project files."""
 
    def clear_file(self, root_dir: str, output_file: str) -> None:
        """Clear/create an empty file at the specified path."""
        output_file = os.path.join(root_dir, output_file)
        parent_dir = os.path.dirname(output_file)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("")

    def write_to_files(self, content: str, output_file: str) -> None:
        """Write content to a file, creating directories as needed."""
        if not isinstance(content, str):
            content = str(content)  
        # Only join with root_dir if output_file is not an absolute path
        if not os.path.isabs(output_file):
            output_file = os.path.join(self.root_dir, output_file)
        parent_dir = os.path.dirname(output_file)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_file, "a", encoding="utf-8") as f:  
            f.write(content + "\n")

    def write_to_json(self, content: dict, output_file: str) -> None:
        """Write content as JSON to a file."""
        self.write_to_files(json.dumps(content, indent=2), f"{output_file}.json")
    
    def write_to_md(self, content: str, output_file: str) -> None:
        """Write content as Markdown to a file."""
        self.write_to_files(content, f"{output_file}.md")
    
    def readFiles(self, output_file: str = "read.txt") -> Dict[str, str]:
        """
        Read all files in the root directory and return their contents.
        
        Returns:
            Dict mapping relative file paths to their contents.
            Uses relative paths as keys to avoid filename collisions.
        """
        content_in_all_files: Dict[str, str] = {}
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            files[:] = [f for f in files if f not in self.ignore_files]
            for file in files:
                file_path = os.path.join(root, file)
                # Use relative path as key to avoid filename collisions
                rel_path = os.path.relpath(file_path, self.root_dir)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        content_in_all_files[rel_path] = content
                except Exception:
                    pass
        return content_in_all_files
    
    def print_folder_not_found(self, path: Optional[str] = None) -> bool:        
        check_path = path or self.root_dir
        if not os.path.isdir(check_path):
            print(f"Folder not found: {check_path}")
            return True
        return False

    def getFiles(self) -> list:
        print("\033[31mGet Files\033[0m", self.root_dir)
        all_files = []

        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            print("\033[32mDirs\033[0m", dirs)
            self.write_to_files(f"DIR: {root}", self.output_file)

            for file in files:
                if file not in self.ignore_files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
                    print(f"Writing file: {file_path}")
                    self.write_to_files(file_path,  self.output_file)
        return all_files

    def detect_language(self, filename: str) -> str:
        _, ext = os.path.splitext(filename)
        ext = ext.lower()
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.rs': 'rust',
            '.md': 'markdown',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml'
        }
        return mapping.get(ext, 'unknown')

    def get_manifest(self) -> dict:
        """Return a manifest of files under root_dir with metadata.

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
        """
        manifest = {}
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            files[:] = [f for f in files if f not in self.ignore_files]
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    stat = os.stat(file_path)
                    rel_path = os.path.relpath(file_path, self.root_dir)
                    manifest[rel_path] = {
                        'path': file_path,
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'language': self.detect_language(file)
                    }
                except OSError:
                    # Skip files we can't stat
                    continue

        return manifest
    
    def __init__(
        self, 
        root_dir: str = os.getcwd(), 
        output_file: str = "output.txt",
        ignore_folders: Optional[Set[str]] = None, 
        ignore_files: Optional[Set[str]] = None
    ) -> None:
        """
        Initialize the FileExplorer.
        
        Args:
            root_dir: Root directory to explore
            output_file: Default output file name
            ignore_folders: Set of folder names to ignore
            ignore_files: Set of file names to ignore
        """
        if ignore_folders is None:
            ignore_folders = {"venv", "__pycache__", "output", "node_modules", ".git"}
        if ignore_files is None:
            ignore_files = { ".env", ".gitignore", ".DS_Store"}
            
        self.output_file = f"output/{output_file}.txt"
        self.root_dir = root_dir 
        self.ignore_folders = ignore_folders
        self.ignore_files = ignore_files
        
        if not self.print_folder_not_found(root_dir):
            self.clear_file(self.root_dir, self.output_file)
