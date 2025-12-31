from typing import Union
import os
import zipfile
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
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

# Use parent directory for uploads/extracted to avoid triggering FastAPI reload
BASE_DIR = os.path.dirname(os.getcwd())  # Parent of backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
EXTRACT_DIR = os.path.join(BASE_DIR, "extracted")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_ZIP_DIR = os.path.join(OUTPUT_DIR, "zip")

# Track processing status for each session
processing_status: dict[str, dict] = {}

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(OUTPUT_ZIP_DIR, exist_ok=True)


def summarizer(folder_to_be_summarized: str, name: str, session_id: str) -> None:
    """Run summarization in background with session tracking."""
    try:
        processing_status[session_id]["status"] = "processing"
        # Pass processing_status and output_dir for progress updates
        Summarize(
            folder_to_be_summarized, 
            name, 
            session_id, 
            processing_status,
            output_base_dir=OUTPUT_DIR
        ).summarize()
        processing_status[session_id]["status"] = "completed"
        # Zip the folder after completion
        zip_folder(name, session_id)
    except Exception as e:
        processing_status[session_id]["status"] = "failed"
        processing_status[session_id]["error"] = str(e)


def zip_folder(name: str, session_id: str) -> str:
    """Zip the output folder for a given session."""
    # Use session_id in output path for multi-session isolation
    folder_path = os.path.join(OUTPUT_DIR, session_id, name)
    
    # Validate folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Output folder not found: {folder_path}")
    
    zip_name = os.path.join(OUTPUT_ZIP_DIR, f"{session_id}_{name}")
    print(f"Zipping folder {folder_path}")
    shutil.make_archive(zip_name, 'zip', folder_path)
    print(f"Zipped folder to {zip_name}.zip")
    
    if session_id in processing_status:
        processing_status[session_id]["download_name"] = f"{session_id}_{name}"
    
    return f"{zip_name}.zip"


@app.get("/")
def read_root() -> dict:
    return {"status": "running"}


@app.get("/download/{name}")
async def download_zip(name: str) -> FileResponse:
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


@app.get("/status/{session_id}")
async def get_status(session_id: str) -> dict:
    """
    Get the processing status for a given session.
    """
    if session_id not in processing_status:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found.")
    return processing_status[session_id]


@app.get("/sessions")
async def list_sessions() -> dict:
    """
    List all active processing sessions and their statuses.
    """
    return {
        "sessions": list(processing_status.values()),
        "total": len(processing_status)
    }


@app.post("/upload")
async def post_upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)) -> dict:
    """
    Accept a ZIP file upload and extract its contents.
    Uses unique session IDs for multi-user isolation.
    """
    # Generate unique session ID for this upload
    session_id = str(uuid.uuid4())
    
    # Initialize processing status
    processing_status[session_id] = {
        "status": "uploading",
        "filename": file.filename,
        "session_id": session_id
    }
    
    # Validate file type
    if not file.filename or not file.filename.endswith(".zip"):
        processing_status[session_id]["status"] = "failed"
        processing_status[session_id]["error"] = "Only ZIP files are allowed."
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed.")

    # Save the uploaded file with session-specific path
    session_upload_dir = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(session_upload_dir, exist_ok=True)
    file_path = os.path.join(session_upload_dir, str(file.filename))
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract the ZIP file to session-specific directory
    name = os.path.splitext(os.path.basename(file.filename))[0]
    extract_path = os.path.join(EXTRACT_DIR, session_id, name)
    os.makedirs(extract_path, exist_ok=True)

    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(extract_path)
    except zipfile.BadZipFile:
        processing_status[session_id]["status"] = "failed"
        processing_status[session_id]["error"] = "Invalid ZIP file."
        raise HTTPException(status_code=400, detail="Invalid ZIP file.")

    # Check if the extracted folder exists
    folder_to_be_summarized = extract_path
    
    # Look for nested folder with same name as zip
    nested_folder = os.path.join(extract_path, name)
    if os.path.exists(nested_folder) and os.path.isdir(nested_folder):
        folder_to_be_summarized = nested_folder
    
    if not os.path.exists(folder_to_be_summarized):
        processing_status[session_id]["status"] = "failed"
        processing_status[session_id]["error"] = f"Extracted folder not found: {folder_to_be_summarized}"
        raise HTTPException(status_code=400, detail=f"Extracted folder not found.")

    processing_status[session_id]["status"] = "queued"
    
    # Run summarization in background so the response returns immediately
    background_tasks.add_task(summarizer, folder_to_be_summarized, name, session_id)
    
    return {
        "message": "File uploaded, processing started.",
        "filename": file.filename,
        "session_id": session_id,
        "status": processing_status[session_id]["status"]
    }
    