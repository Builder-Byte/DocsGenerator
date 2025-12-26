from file_explorer_cli import FileExplorer
from dependency_generator import DependencyGenerator
from openrouter_client import OpenRouterClient
from docs_creator import DocsCreator
try:
    from gemini_client import GeminiClient  # optional, not used
except Exception:
    GeminiClient = None
    
import time
import shutil
import os


#folder_to_summarize = "mini_project"  # Replace with the desired folder name

class Summarize():
    
    def summarize(self):
        print("Beginning...")       
        t = self.File.readFiles()
        client = OpenRouterClient()
        no_of_files = len(t.keys())
        index =1 
        
        
        for a in t.keys():
            if index >1:
                return 
            out = DependencyGenerator().summarize_file(t[a])
            out['file_name'] = a
            while True:
                try:
                    out["summary"] = client.summarize(t[a])
                    break
                except Exception as e:
                    print(f"Error: {e}. Retrying...")
                    time.sleep(5)

            DocsCreator().json_to_markdown(out, f"{self.output_folder}/md/{a}.md")
            self.File.write_to_json(content=out, output_file=f"{self.output_folder}/json/{a}")
            print(f"{index} of {no_of_files} completed...")
            index += 1
             
    def __init__(self, folder_to_summarize,ouptut_folder) -> None:
        
        self.output_folder = os.path.join(os.getcwd(), f"output/{ouptut_folder}")
        #if os.path.exists(self.output_folder):
        #    shutil.rmtree(self.output_folder)    
        os.makedirs(self.output_folder, exist_ok=True)
        
        self.File = FileExplorer(
            root_dir=os.path.join(folder_to_summarize),
            ignore_folders={"venv", "__pycache__", "output", "dependency_generator"}
        )
        
#Summarize('mini_project').summarize()