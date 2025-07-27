# 1. ALL IMPORTS AT THE TOP
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import uvicorn
import os
import tempfile
from pypdf import PdfReader
import io

# test comment

# 2. PYDANTIC MODELS DEFINED ONCE
# This model is for creating a new entry (what the API receives)
class JournalEntryCreate(BaseModel):
    title: str
    content: str

# This model is for representing a stored entry (what the API returns)
class JournalEntry(BaseModel):
    id: int
    title: str
    content: str
    timestamp: str

# 3. APP INITIALIZATION (ONCE)
app = FastAPI(title="CuraData", description="Medical Document Analyzer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add template and static file support
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# 4. IN-MEMORY STORAGE (DATABASE REPLACEMENT)
journal_entries: List[JournalEntry] = []


# 5. YOUR ROUTES (NO DUPLICATES)

# --- Page Routes ---
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})
    
@app.get("/journal", response_class=HTMLResponse)
async def journal_page(request: Request):
    # It's better to use a template file for large HTML content
    return templates.TemplateResponse("journal.html", {"request": request})


# --- Journal API Routes ---

@app.post("/api/journal/entry", response_model=JournalEntry, status_code=201)
async def save_journal_entry(entry: JournalEntryCreate):
    """
    Saves a new journal entry.
    Receives a title and content, returns the full entry with new ID and timestamp.
    """
    try:
        new_entry = JournalEntry(
            id=len(journal_entries) + 1,
            title=entry.title,
            content=entry.content,
            timestamp=datetime.now().isoformat()
        )
        journal_entries.append(new_entry)
        return new_entry
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/journal/entries", response_model=List[JournalEntry])
async def get_all_journal_entries():
    """
    Returns all saved journal entries.
    """
    return journal_entries
    
@app.post("/api/upload-advanced")
async def upload_advanced(file: UploadFile = File(...)):
    # Your enhanced upload logic...
    pass  # (I've removed the implementation for brevity)


# ===== START: ADD THE DEBUGGING ROUTE HERE (Lines 99-118) =====
@app.get("/debug-templates")
def debug_templates():
    """
    A temporary route to check if template files are found.
    """
    template_dir = "app/templates"
    try:
        files = os.listdir(template_dir)
        return {
            "message": "Successfully listed files.",
            "directory": template_dir,
            "files_found": files
        }
    except FileNotFoundError:
        # This part is crucial for debugging if the directory isn't found
        return {
            "error": "Directory not found!",
            "directory_searched": template_dir,
            "current_working_directory": os.getcwd()
        }
    except Exception as e:
        return {"error": str(e)}
# ===== END: ADD THE DEBUGGING ROUTE HERE =====


# --- Health check and test routes ---
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "CuraData API"}

@app.get("/test")
def test():
    return {"message": "Test route works!", "status": "success"}


# --- Other API Routes from your file ---
@app.post("/api/upload-advanced")
async def upload_advanced(file: UploadFile = File(...)):
    # Your enhanced upload logic...
    pass  # (I've removed the implementation for brevity)


# --- Health check and test routes ---
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "CuraData API"}

@app.get("/test")
def test():
    return {"message": "Test route works!", "status": "success"}


# 6. RUN THE APP (at the very end)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

