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

# Health Analyzer imports
from typing import Optional, Dict, Any
import logging
from app.health_analyzer import HealthAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# After line 33, ADD ALL OF THIS:

# Request/Response models for health analysis
class HealthAnalysisRequest(BaseModel):
    lab_text: str
    user_id: Optional[str] = None
    analysis_type: Optional[str] = "comprehensive"

class HealthAnalysisResponse(BaseModel):
    success: bool
    extracted_values: Dict[str, Any]
    detailed_analysis: Dict[str, Any]
    summary: Dict[str, Any]
    error_message: Optional[str] = None

# Initialize the health analyzer
health_analyzer = HealthAnalyzer()

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
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})
    

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
    try:
        print(f"Received file upload: {file.filename}")
        
        # Extract text from PDF
        try:
            pdf_content = await file.read()
            if not pdf_content:
                raise HTTPException(status_code=400, detail="Uploaded file is empty")
                
            pdf_file = io.BytesIO(pdf_content)
            
            try:
                pdf_reader = PdfReader(pdf_file)
                print(f"Successfully created PDF reader, number of pages: {len(pdf_reader.pages)}")
                
                extracted_text = ""
                for i, page in enumerate(pdf_reader.pages, 1):
                    try:
                        page_text = page.extract_text() or ""
                        print(f"Page {i} text length: {len(page_text)} characters")
                        extracted_text += page_text + "\n"
                    except Exception as page_error:
                        print(f"Error extracting text from page {i}: {str(page_error)}")
                
                print(f"Total extracted text length: {len(extracted_text)} characters")
                
                if not extracted_text.strip():
                    raise HTTPException(status_code=400, detail="No text could be extracted from the PDF")
                
            except Exception as pdf_error:
                print(f"Error reading PDF: {str(pdf_error)}")
                raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(pdf_error)}")
            
            # Analyze the extracted text
            try:
                print("Starting health analysis...")
                analysis_results = health_analyzer.analyze_lab_report(extracted_text)
                print("Analysis completed successfully")
                
                # Prepare response
                response = {
                    "success": True,
                    "extracted_text": extracted_text[:500],  # Preview
                    "extracted_biomarkers": analysis_results.get('extracted_biomarkers', {}),
                    "analysis": analysis_results.get('analysis', {}),
                    "summary": analysis_results.get('summary', {})
                }
                
                print(f"Response prepared with {len(analysis_results.get('extracted_biomarkers', {}))} biomarkers")
                return response
                
            except Exception as analysis_error:
                print(f"Error during analysis: {str(analysis_error)}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"Error during analysis: {str(analysis_error)}")
                
        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error processing file: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in upload_advanced: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


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


# --- Health Analysis Routes ---
@app.post("/api/health-analysis", response_model=HealthAnalysisResponse)
async def analyze_health_data(request: HealthAnalysisRequest):
    """
    Analyze lab report text and extract key biomarkers
    """
    try:
        logger.info(f"Received analysis request for user: {request.user_id}")
        
        # Validate input
        if not request.lab_text or len(request.lab_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Lab text is too short or empty")
        
        # Process the lab report
        results = health_analyzer.analyze_lab_report(request.lab_text)
        
        # Log if no biomarkers were found
        if not results['extracted_biomarkers']:
            logger.warning("No biomarkers extracted from the provided text")
            
        # Add success flag and format response
        response = HealthAnalysisResponse(
            success=True,
            extracted_values=results['extracted_biomarkers'],
            detailed_analysis=results['analysis'],
            summary=results['summary']
        )
        
        logger.info(f"Successfully analyzed {len(results['extracted_biomarkers'])} biomarkers")
        return response
        
    except Exception as e:
        logger.error(f"Error in health analysis: {str(e)}")
        return HealthAnalysisResponse(
            success=False,
            extracted_values={},
            detailed_analysis={},
            summary={'error': str(e)},
            error_message=f"Analysis failed: {str(e)}"
        )

@app.post("/api/analyze-biomarker")
async def analyze_single_biomarker(
    biomarker_type: str,
    value: float,
    unit: str
):
    """
    Analyze a single biomarker value
    """
    try:
        if biomarker_type == "vitamin_d":
            result = health_analyzer.analyze_vitamin_d_enhanced(value, unit)
        elif biomarker_type == "neutrophils":
            result = health_analyzer.analyze_neutrophils_enhanced(value, unit)
        elif biomarker_type == "lymphocytes":
            result = health_analyzer.analyze_lymphocytes_enhanced(value, unit)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown biomarker type: {biomarker_type}")
        
        return {"success": True, "analysis": result}
        
    except Exception as e:
        logger.error(f"Error analyzing biomarker: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health-analyzer-status")
async def check_analyzer_status():
    """
    Check if the health analyzer is properly initialized
    """
    try:
        # Test the analyzer with a simple extraction
        test_text = "Vitamin D: 25 ng/mL"
        test_result = health_analyzer.extract_biomarkers_from_text(test_text)
        
        return {
            "status": "healthy",
            "analyzer_version": "2.0",
            "supported_biomarkers": list(health_analyzer.biomarker_aliases.keys()),
            "test_extraction": test_result
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

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
