from typing import Union
import os
import zipfile
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException
from summarize import Summarize
app = FastAPI()

UPLOAD_DIR = "uploads"
EXTRACT_DIR = "extracted"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)

def summarizer(folder_to_be_summarized: str,name:str):
    Summarize(folder_to_be_summarized, name).summarize()
    
def zip_folder(name: str):
    folder_path = os.path.join(os.getcwd(), "output", name)
    output_zip_dir = os.path.join(os.getcwd(), "output_zip")
    os.makedirs(output_zip_dir, exist_ok=True)
    zip_name = os.path.join(output_zip_dir, name)
    print(f"Zipping folder {folder_path}")
    shutil.make_archive(zip_name, 'zip', folder_path)
    print(f"Zipped folder to {zip_name}.zip")
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/upload")
async def post_upload(file: UploadFile = File(...)):
    """
    Accept a ZIP file upload and extract its contents.
    """
    # Validate file type
    if not file.filename or not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed.")

    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, str(file.filename))
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract the ZIP file
    extract_path = os.path.join(EXTRACT_DIR, os.path.splitext(file.filename)[0])
    os.makedirs(extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file.")

    name = os.path.splitext(os.path.basename(file.filename))[0]
    folder_to_be_summarized = f"{extract_path}/{name}"
    summarizer(folder_to_be_summarized,name)
    zip_folder(name)
    return {
        "message": "File uploaded and extracted successfully.",
        "filename": file.filename,
        "extracted_to": extract_path,
        "folder_to_be_summarized": folder_to_be_summarized
        }
    