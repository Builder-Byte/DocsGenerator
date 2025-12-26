from typing import Union
import os
import zipfile
import shutil

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from summarize import Summarize

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

UPLOAD_DIR = "uploads"
EXTRACT_DIR = "extracted"
OUTPUT_ZIP_DIR = os.path.join(os.getcwd(), "output", "zip")

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(OUTPUT_ZIP_DIR, exist_ok=True)

def summarizer(folder_to_be_summarized: str,name:str):
    Summarize(folder_to_be_summarized, name).summarize()
    
def zip_folder(name: str) -> str:
    folder_path = os.path.join(os.getcwd(), "output", name)
    zip_name = os.path.join(OUTPUT_ZIP_DIR, name)
    print(f"Zipping folder {folder_path}")
    shutil.make_archive(zip_name, 'zip', folder_path)
    print(f"Zipped folder to {zip_name}.zip")
    return f"{zip_name}.zip"
    

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/download/{name}")
async def download_zip(name: str):
    """
    Download the generated ZIP file by name.
    """
    zip_path = os.path.join(OUTPUT_ZIP_DIR, f"{name}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail=f"ZIP file '{name}.zip' not found.")
    return FileResponse(
        path=zip_path,
        filename=f"{name}.zip",
        media_type="application/zip"
    )


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
    