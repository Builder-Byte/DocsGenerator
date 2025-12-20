import os
import json
class FileExplorer:
 
    def clear_file(self, root_dir, output_file):
        output_file = os.path.join(root_dir, output_file)
        parent_dir = os.path.dirname(output_file)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("")

    def write_to_files(self, content, output_file):
        if type(content) != str:
            content = str(content)  
        output_file = os.path.join(self.root_dir, output_file)
        parent_dir = os.path.dirname(output_file)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(output_file, "a", encoding="utf-8") as f:  
            f.write(content+ "\n")

    def write_to_json(self, content, output_file):
        self.write_to_files(json.dumps(content), f"{output_file}.json")
    
    def write_to_md(self, content, output_file):
        self.write_to_files(json.dumps(content), f"{output_file}.md")
    
    def readFiles(self, output_file="read.txt") -> dict:
        output_file = os.path.join(self.root_dir, output_file) 
        content_in_all_files= {}
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in self.ignore_folders]
            files[:] = [f for f in files if f not in self.ignore_files]
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:  
                    try:
                        content = f.read()
                        content_in_all_files[file] = content
                    except:
                        pass
                    #self.write_to_files(content, output_file)
        return ( content_in_all_files)
    
    def print_folder_not_found(self, path: str | None = None) -> bool:        
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
    
    def __init__(self, root_dir= os.getcwd(), output_file="output.txt",ignore_folders={"venv", "__pycache__", "output"}, 
                 ignore_files={"output.txt", "read.txt",".env", ".gitignore"}):
        self.output_file = "output/"+ f"{output_file}.txt"
        self.root_dir = root_dir 
        self.print_folder_not_found(root_dir)
        self.ignore_folders= ignore_folders
        self.ignore_files = ignore_files
        self.clear_file(self.root_dir, self.output_file)
