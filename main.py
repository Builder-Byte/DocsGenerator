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

output_folder = os.path.join(os.getcwd(), "output")

if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

os.makedirs(output_folder, exist_ok=True)

folder_to_summarize = "mini_project"  # Replace with the desired folder name
File = FileExplorer(
    root_dir=os.path.join(folder_to_summarize),
    ignore_folders={"venv", "__pycache__", "output", "dependency_generator"}
)
t = File.readFiles()
File.write_to_json(t, "output123")

client = OpenRouterClient()
for a in t.keys():
    
    out = DependencyGenerator().summarize_file(t[a])
    out['file_name'] = a
    while True:
        try:
            out["summary"] = client.summarize(t[a])
            break
        except Exception as e:
            print(f"Error: {e}. Retrying...")
            time.sleep(5)
    
    DocsCreator().json_to_markdown(out, f"{output_folder}/md/{a}.md")
    File.write_to_json(content=out, output_file=f"{output_folder}/json/{a}")

