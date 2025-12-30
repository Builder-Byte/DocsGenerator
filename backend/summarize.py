from file_explorer_cli import FileExplorer
from dependency_generator import DependencyGenerator
from openrouter_client import OpenRouterClient
from docs_creator import DocsCreator
    
import time
import shutil
import os
import uuid
from typing import Dict, Optional


#folder_to_summarize = "mini_project"  # Replace with the desired folder name

class Summarize:
    """
    Main class for summarizing code files in a project.
    
    Reads all files from a folder, analyzes them using DependencyGenerator,
    generates AI summaries, and creates Markdown documentation.
    """
    
    # Class-level reference to processing_status dict (set by server)
    processing_status: Optional[Dict] = None
    
    def summarize(self) -> None:
        """
        Process all files in the project and generate documentation.
        
        For each file:
        1. Extract code structure (imports, functions, classes, etc.)
        2. Perform cross-library analysis to link imports to source files
        3. Generate AI summary of the code
        4. Create Markdown and JSON documentation
        """
        print(f"Beginning summarization (session: {self.session_id})...")
        
        # Read all project files
        all_files: Dict[str, str] = self.File.readFiles()
        client = OpenRouterClient()
        dependency_gen = DependencyGenerator()
        docs_creator = DocsCreator()
        
        no_of_files = len(all_files)
        print(f"Found {no_of_files} files to process.")
        
        # Update progress tracking
        self._update_progress(0, no_of_files, "Starting...")
        
        for index, (file_path, content) in enumerate(all_files.items(), start=1):
            print(f"Processing {index}/{no_of_files}: {file_path}")
            self._update_progress(index, no_of_files, file_path)
            
            # Generate code analysis with cross-library function details
            out = dependency_gen.summarize_file(content, project_files=all_files)
            out['file_name'] = file_path
            
            # Generate AI summary with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    out["summary"] = client.summarize(content)
                    break
                except Exception as e:
                    print(f"Error on attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        print("Retrying...")
                        time.sleep(5)
                    else:
                        out["summary"] = f"Error generating summary: {e}"

            # Create safe filename for output (replace / with _)
            safe_filename = file_path.replace('/', '_').replace('\\', '_')
            
            # Generate documentation
            docs_creator.json_to_markdown(out, f"{self.output_folder}/md/{safe_filename}.md")
            self.File.write_to_json(content=out, output_file=f"{self.output_folder}/json/{safe_filename}")
            
            print(f"Completed {index}/{no_of_files}: {file_path}")
    
    def _update_progress(self, current: int, total: int, current_file: str) -> None:
        """Update progress in the shared processing_status dict."""
        if self.processing_status is not None and self.session_id in self.processing_status:
            self.processing_status[self.session_id]["progress"] = {
                "current": current,
                "total": total,
                "current_file": current_file,
                "percentage": round((current / total) * 100) if total > 0 else 0
            }
             
    def __init__(
        self, 
        folder_to_summarize: str, 
        output_folder: str, 
        session_id: Optional[str] = None,
        processing_status: Optional[Dict] = None,
        output_base_dir: Optional[str] = None
    ) -> None:
        """
        Initialize the Summarize class.
        
        Args:
            folder_to_summarize: Path to the folder containing source code
            output_folder: Name of the output folder for generated docs
            session_id: Optional unique session identifier for multi-user support
            processing_status: Optional reference to shared status dict for progress updates
            output_base_dir: Optional base directory for output files
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.processing_status = processing_status
        
        # Use provided base dir or default to cwd/output
        base_dir = output_base_dir or os.path.join(os.getcwd(), "output")
        # Use session_id in path for multi-session isolation
        self.output_folder = os.path.join(base_dir, self.session_id, output_folder)
        
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(f"{self.output_folder}/md", exist_ok=True)
        os.makedirs(f"{self.output_folder}/json", exist_ok=True)
        
        self.File = FileExplorer(
            root_dir=folder_to_summarize,
            ignore_folders={"venv", "__pycache__", "node_modules", ".git"}
        )
        
        print(f"Initialized Summarize for: {folder_to_summarize}")
        print(f"Output folder: {self.output_folder}")
        print(f"Session ID: {self.session_id}")
        
#Summarize('mini_project').summarize()