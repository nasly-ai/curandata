from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import tempfile
from pypdf import PdfReader
import io

# Initialize FastAPI app
app = FastAPI(title="CuraData", description="Medical Document Analyzer")

# Add template and static file support
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Homepage route
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Results page
@app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request):
    return templates.TemplateResponse("results.html", {"request": request})

# Analysis page
@app.get("/analysis", response_class=HTMLResponse)
async def analysis_page(request: Request):
    return templates.TemplateResponse("analysis.html", {"request": request})

# API Routes

@app.post("/api/upload-advanced")
async def upload_advanced(file: UploadFile = File(...)):
    """Enhanced upload with OCR and text extraction"""
    try:
        # Validate file type
        allowed_types = ["application/pdf", "image/jpeg", "image/jpg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Read file content
        file_content = await file.read()
        
        # Extract text based on file type
        extracted_text = ""
        
        if file.content_type == "application/pdf":
            # Extract text from PDF using pypdf
            try:
                pdf_file = io.BytesIO(file_content)
                pdf_reader = PdfReader(pdf_file)
                
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n"
                    
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")
                
        elif file.content_type.startswith("image/"):
            # For images, you would typically use OCR here
            # This is a placeholder - you'd implement Google Vision API or similar
            extracted_text = "Image OCR processing would happen here. Please implement Google Vision API integration."
        
        # Return extracted text
        return {
            "success": True,
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(file_content),
            "text": extracted_text.strip(),
            "message": "Document processed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/api/health-analysis")
async def health_analysis(data: dict):
    """AI analysis of medical text"""
    try:
        text = data.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="No text provided for analysis")
        
        # This is where you'd integrate with your AI service
        # For now, return a mock analysis
        analysis = {
            "summary": "This appears to be a medical document. The text has been processed and analyzed for key medical information.",
            "key_findings": [
                "Medical terminology detected",
                "Test results or clinical observations present",
                "Professional medical language identified"
            ],
            "recommendations": [
                "Please consult with your healthcare provider to discuss these results",
                "Keep this analysis for your medical records",
                "Schedule a follow-up appointment if recommended"
            ],
            "confidence": 0.85,
            "processed_at": "2025-07-26T00:00:00Z"
        }
        
        return {
            "success": True,
            "analysis": analysis,
            "original_text_length": len(text)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Basic file upload and text extraction"""
    try:
        # Save the uploaded file temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(await file.read())
        temp_file.close()

        # Extract text from PDF using pypdf
        text = ""
        try:
            with open(temp_file.name, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"PDF processing error: {str(e)}")
        finally:
            # Clean up temp file
            os.remove(temp_file.name)

        return {"filename": file.filename, "text": text}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload error: {str(e)}")

# Test routes
@app.get("/test")
def test():
    return {"message": "working"}

@app.get("/test_route")
async def test_route():
    return {"message": "Test route works!", "status": "success"}

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "CuraData API",
        "version": "1.0.0"
    }

# API documentation
@app.get("/api/info")
async def api_info():
    return {
        "name": "CuraData API",
        "description": "Medical Document Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/upload-advanced": "Upload and process medical documents",
            "POST /api/health-analysis": "Analyze medical text with AI",
            "POST /upload": "Basic file upload",
            "GET /": "Homepage",
            "GET /results": "Analysis results page",
            "GET /health": "Health check"
        }
    }

from pydantic import BaseModel
from fastapi import APIRouter

class JournalEntry(BaseModel):
    id: int
    title: str
    content: str

# Journal/storage functionality (if needed)
journal_entries = []

class JournalEntry:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

@app.post("/save_journal_entry")
async def save_journal_entry(entry: JournalEntry):
    # You can access the data with entry.title, entry.content, etc.
    journal_entries.append({"title": entry.title, "content": entry.content})
    return {"message": "Entry saved!", "entry": entry.dict()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

app = FastAPI()

# Add new routes:
@app.post("/api/upload-advanced")  # Enhanced upload with OCR
@app.post("/api/health-analysis")  # AI analysis
@app.get("/scanner")               # Camera scanner page
@app.get("/analysis")              # AI analysis results page

# ==== Route: Upload PDF and Extract Text ====
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(await file.read())
    temp_file.close()

    # Extract text from PDF using PyMuPDF
    text = ""
    doc = PdfReader(temp_file.name)
    for page in doc:
        text += page.extract_text()

    os.remove(temp_file.name)

    return {"filename": file.filename, "text": text}

# ==== Other Routes (like /journal) ====
from pydantic import BaseModel
from fastapi import APIRouter

class JournalEntry(BaseModel):
    id: int
    title: str
    
@app.get("/journal", response_class=HTMLResponse)
async def journal_page():
    return """<!DOCTYPE html> ... your journal HTML ..."""

from pydantic import BaseModel
from fastapi import APIRouter

class JournalEntry(BaseModel):
    id: int
    title: str
    timestamp: str  # or datetime if you want automatic time parsing


@app.post("/save_journal_entry")
async def save_journal_entry(entry: JournalEntry):
    # You can access the data with entry.title, entry.content, etc.
    return {"message": "Entry saved!", "entry": entry.dict()}

@app.get("/test")
def test():
    return {"message": "working"}

@app.get("/test")
async def test_route():
    return {"message": "Test route works!", "status": "success"}

# ===== ADD THIS AFTER YOUR CURRENT LINE 22 =====

# Storage for journal entries and bloodwork
journal_entries = []
bloodwork_submissions = []

# ===== YOUR EXISTING ROUTES STAY THE SAME =====
# (Keep your existing @app.get("/") and @app.post("/upload/") routes)

# ===== ADD THIS NEW JOURNAL ROUTE =====

from pydantic import BaseModel
from fastapi import APIRouter

class JournalEntry(BaseModel):
    id: int
    title: str
    
@app.get("/journal", response_class=HTMLResponse)
async def journal_page():
    """Health Journal Calendar Page"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health Journal - CuraData</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { max-width: 1000px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: white; margin-bottom: 2rem; }
            .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
            .journal-section {
                background: rgba(255, 255, 255, 0.95);
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .calendar-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 2rem;
            }
            .nav-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 50%;
                cursor: pointer;
                font-size: 1.2rem;
            }
            .calendar-grid {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 1px;
                background: #ddd;
                border-radius: 10px;
                overflow: hidden;
            }
            .calendar-day {
                background: white;
                padding: 1rem;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                min-height: 80px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }
            .calendar-day:hover { background: #f0f8ff; }
            .calendar-day.today { background: #667eea; color: white; }
            .day-headers {
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 1px;
                margin-bottom: 1rem;
                text-align: center;
                font-weight: bold;
            }
            .modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 1000;
            }
            .modal-content {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                width: 90%;
                max-width: 500px;
                max-height: 80vh;
                overflow-y: auto;
            }
            .mood-selector {
                display: flex;
                gap: 1rem;
                margin: 1rem 0;
                flex-wrap: wrap;
            }
            .mood-btn {
                padding: 0.5rem 1rem;
                border: 2px solid #ddd;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .mood-btn:hover, input[type="radio"]:checked + .mood-btn {
                border-color: #667eea;
                background: #e8f4fd;
            }
            input[type="radio"] { display: none; }
            .supplement-checkboxes, .symptom-checkboxes {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 0.5rem;
                margin: 1rem 0;
            }
            .hidden { display: none; }
            .btn-primary {
                background: #667eea;
                color: white;
                border: none;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
            }
            .btn-secondary {
                background: #ccc;
                color: #333;
                border: none;
                padding: 0.8rem 1.5rem;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
            }
            .form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 2rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📅 Health Journal</h1>
                <p>Track your daily symptoms and supplement effects</p>
            </div>

            <div class="journal-section">
                <div class="calendar-header">
                    <button class="nav-btn" onclick="changeMonth(-1)">‹</button>
                    <h2 id="currentMonth"></h2>
                    <button class="nav-btn" onclick="changeMonth(1)">›</button>
                </div>

                <div class="day-headers">
                    <div>Sun</div><div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div>
                </div>
                
                <div class="calendar-grid" id="calendarGrid">
                    <!-- Calendar days will be generated here -->
                </div>

                <div style="text-align: center; margin-top: 2rem;">
                    <a href="/" style="color: #667eea; text-decoration: none;">← Back to Home</a>
                </div>
            </div>
        </div>

        <!-- Modal for adding entries -->
        <div id="entryModal" class="modal hidden">
            <div class="modal-content">
                <h3>📝 Log Entry for <span id="selectedDate"></span></h3>
                <form id="entryForm">
                    <div>
                        <label>How did you feel today?</label>
                        <div class="mood-selector">
                            <input type="radio" id="great" name="mood" value="great">
                            <label for="great" class="mood-btn">😄 Great</label>
                            
                            <input type="radio" id="good" name="mood" value="good">
                            <label for="good" class="mood-btn">😊 Good</label>
                            
                            <input type="radio" id="okay" name="mood" value="okay">
                            <label for="okay" class="mood-btn">😐 Okay</label>
                            
                            <input type="radio" id="poor" name="mood" value="poor">
                            <label for="poor" class="mood-btn">😔 Poor</label>
                        </div>
                    </div>

                    <div>
                        <label>Supplements taken yesterday:</label>
                        <div class="supplement-checkboxes">
                            <label><input type="checkbox" name="supplements" value="vitaminD"> Vitamin D</label>
                            <label><input type="checkbox" name="supplements" value="vitaminC"> Vitamin C</label>
                            <label><input type="checkbox" name="supplements" value="iron"> Iron</label>
                            <label><input type="checkbox" name="supplements" value="omega3"> Omega-3</label>
                        </div>
                    </div>

                    <div>
                        <label>Symptoms experienced:</label>
                        <div class="symptom-checkboxes">
                            <label><input type="checkbox" name="symptoms" value="fatigue"> Fatigue</label>
                            <label><input type="checkbox" name="symptoms" value="headache"> Headache</label>
                            <label><input type="checkbox" name="symptoms" value="nausea"> Nausea</label>
                            <label><input type="checkbox" name="symptoms" value="joint-pain"> Joint Pain</label>
                        </div>
                    </div>

                    <div>
                        <label for="notes">Notes:</label>
                        <textarea id="notes" name="notes" rows="3" style="width: 100%; padding: 0.5rem; border-radius: 8px; border: 1px solid #ddd;"></textarea>
                    </div>

                    <div class="form-actions">
                        <button type="button" class="btn-secondary" onclick="closeModal()">Cancel</button>
                        <button type="submit" class="btn-primary">Save Entry</button>
                    </div>
                </form>
            </div>
        </div>

        <script>
            let currentDate = new Date();
            let selectedDate = null;

            function generateCalendar() {
                const grid = document.getElementById('calendarGrid');
                const monthHeader = document.getElementById('currentMonth');
                
                const year = currentDate.getFullYear();
                const month = currentDate.getMonth();
                
                monthHeader.textContent = new Date(year, month).toLocaleDateString('en-US', { 
                    month: 'long', 
                    year: 'numeric' 
                });
                
                const firstDay = new Date(year, month, 1).getDay();
                const daysInMonth = new Date(year, month + 1, 0).getDate();
                
                grid.innerHTML = '';
                
                for (let i = 0; i < firstDay; i++) {
                    const emptyDay = document.createElement('div');
                    emptyDay.className = 'calendar-day';
                    grid.appendChild(emptyDay);
                }
                
                for (let day = 1; day <= daysInMonth; day++) {
                    const dayElement = document.createElement('div');
                    dayElement.className = 'calendar-day';
                    dayElement.textContent = day;
                    
                    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                    
                    const today = new Date();
                    if (year === today.getFullYear() && month === today.getMonth() && day === today.getDate()) {
                        dayElement.classList.add('today');
                    }
                    
                    dayElement.onclick = () => openModal(dateStr);
                    grid.appendChild(dayElement);
                }
            }
            
            function changeMonth(direction) {
                currentDate.setMonth(currentDate.getMonth() + direction);
                generateCalendar();
            }
            
            function openModal(date) {
                selectedDate = date;
                document.getElementById('selectedDate').textContent = new Date(date).toLocaleDateString();
                document.getElementById('entryModal').classList.remove('hidden');
            }
            
            function closeModal() {
                document.getElementById('entryModal').classList.add('hidden');
            }
            
            document.getElementById('entryForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const entry = {
                    date: selectedDate,
                    mood: formData.get('mood'),
                    supplements: formData.getAll('supplements'),
                    symptoms: formData.getAll('symptoms'),
                    notes: formData.get('notes')
                };
                
                try {
                    const response = await fetch('/api/journal/entry', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(entry)
                    });
                    
                    if (response.ok) {
                        alert('Entry saved successfully!');
                        closeModal();
                    }
                } catch (error) {
                    alert('Failed to save entry');
                }
            });
            
            generateCalendar();
        </script>
    </body>
    </html>
    """
from pydantic import BaseModel
from fastapi import APIRouter

class JournalEntry(BaseModel):
    id: int
    title: str
    
# Add the API endpoint after the journal route
@app.post("/api/journal/entry")
async def save_journal_entry(entry: JournalEntry):
    try:
        entry_data = {
            **entry.dict(),
            "timestamp": datetime.now().isoformat(),
            "id": len(journal_entries) + 1
        }
        journal_entries.append(entry_data)
        return {"success": True, "message": "Journal entry saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi.responses import HTMLResponse
from fastapi import UploadFile, File

# Upload form page
@app.get("/scanner", response_class=HTMLResponse)
async def scanner_page():
    return """
    <html>
    <head>
        <title>Upload PDF for OCR - CuraData</title>
    </head>
    <body>
        <h2>Upload Medical Report (PDF)</h2>
        <form action="/scanner" enctype="multipart/form-data" method="post">
            <input type="file" name="file" accept="application/pdf">
            <input type="submit" value="Scan PDF">
        </form>
    </body>
    </html>
    """

# Handle file upload and scan
@app.post("/scanner", response_class=HTMLResponse)
async def scan_uploaded_file(file: UploadFile = File(...)):
    # Placeholder logic: Add your Google Vision OCR function here
    scanned_text = f"Uploaded file: {file.filename} (📄 OCR logic goes here)"

    return HTMLResponse(content=f"<pre>{scanned_text}</pre>", status_code=200)


# ===== ENHANCED UPLOAD WITH OCR AND AI ANALYSIS =====
@app.post("/api/upload-advanced")
async def upload_advanced(file: UploadFile = File(...)):
    """Enhanced upload with OCR and AI analysis"""
    try:
        # Read file content
        content = await file.read()
        
        # Save temporarily
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file.write(content)
        temp_file.close()
        
        # Extract text using Google Vision API (you'll need to set up credentials)
        extracted_text = await extract_text_from_image(temp_file.name)
        
        # Analyze biomarkers
        biomarkers = analyze_biomarkers_from_text(extracted_text)
        
        # Get AI health analysis
        health_analysis = await get_health_gpt_analysis(extracted_text, biomarkers)
        
        # Clean up
        os.remove(temp_file.name)
        
        return {
            "success": True,
            "filename": file.filename,
            "extracted_text": extracted_text,
            "biomarkers": biomarkers,
            "health_analysis": health_analysis
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# ===== HELPER FUNCTIONS =====
async def extract_text_from_image(image_path):
    """Extract text using Google Vision API"""
    try:
        # For now, return mock data - you'll integrate Google Vision API
        return "Sample extracted text from lab report. Vitamin D: 25 ng/mL, Lymphocytes: 35%, Neutrophils: 58%"
    except Exception as e:
        return f"OCR Error: {str(e)}"

def analyze_biomarkers_from_text(text):
    """Analyze biomarkers from extracted text"""
    import re
    
    biomarkers = {}
    
    # Define patterns for common biomarkers
    patterns = {
        'vitamin_d': r'Vitamin D[^:]*:\s*(\d+\.?\d*)',
        'lymphocytes': r'Lymphocytes[^:]*:\s*(\d+\.?\d*)\s*%',
        'neutrophils': r'Neutrophils[^:]*:\s*(\d+\.?\d*)\s*%',
        'hemoglobin': r'Hemoglobin[^:]*:\s*(\d+\.?\d*)',
        'glucose': r'Glucose[^:]*:\s*(\d+\.?\d*)',
        'cholesterol': r'Cholesterol[^:]*:\s*(\d+\.?\d*)'
    }
    
    for biomarker, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            biomarkers[biomarker] = float(match.group(1))
    
    return biomarkers

async def get_health_gpt_analysis(extracted_text, biomarkers):
    """Get AI health analysis using OpenAI or similar"""
    try:
        # Mock AI analysis - you'll integrate with OpenAI API
        analysis = "Based on your lab results, here are some insights:\n\n"
        
        if biomarkers:
            for biomarker, value in biomarkers.items():
                if biomarker == 'vitamin_d':
                    if value < 30:
                        analysis += f"• Your Vitamin D level ({value} ng/mL) is below optimal. Consider supplementation and more sun exposure.\n"
                    else:
                        analysis += f"• Your Vitamin D level ({value} ng/mL) is within a good range.\n"
                
                elif biomarker == 'lymphocytes':
                    if value < 20 or value > 40:
                        analysis += f"• Your lymphocyte percentage ({value}%) is outside the normal range (20-40%). Consult your healthcare provider.\n"
                    else:
                        analysis += f"• Your lymphocyte levels ({value}%) are normal.\n"
        
        analysis += "\n💡 Remember: This is AI-generated analysis for educational purposes. Always consult with your healthcare provider for medical advice."
        
        return analysis
        
    except Exception as e:
        return f"AI Analysis Error: {str(e)}"

# ===== HEALTH GPT CHAT INTERFACE =====
@app.get("/health-gpt", response_class=HTMLResponse)
async def health_gpt_page():
    """Health GPT Chat Interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Health GPT - CuraData</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: white; margin-bottom: 2rem; }
            .header h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
            .chat-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 2rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                height: 600px;
                display: flex;
                flex-direction: column;
            }
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 1rem;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                margin-bottom: 1rem;
                background: #f8f9fa;
            }
            .message {
                margin-bottom: 1rem;
                padding: 1rem;
                border-radius: 10px;
                max-width: 80%;
            }
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
            }
            .ai-message {
                background: #e8f4fd;
                color: #333;
            }
            .input-container {
                display: flex;
                gap: 1rem;
                align-items: flex-end;
            }
            .chat-input {
                flex: 1;
                padding: 1rem;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 1rem;
                resize: none;
                font-family: inherit;
            }
            .chat-input:focus {
                outline: none;
                border-color: #667eea;
            }
            .send-btn {
                background: #667eea;
                color: white;
                border: none;
                padding: 1rem 2rem;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            .send-btn:hover {
                background: #5a6fd8;
                transform: translateY(-2px);
            }
            .typing {
                color: #666;
                font-style: italic;
                padding: 1rem;
            }
            .nav-links {
                text-align: center;
                margin-top: 2rem;
                padding-top: 2rem;
                border-top: 1px solid #e0e0e0;
            }
            .nav-links a {
                color: #667eea;
                text-decoration: none;
                margin: 0 1rem;
                font-weight: 500;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Health GPT</h1>
                <p>Ask questions about your health and lab results</p>
            </div>

            <div class="chat-container">
                <div id="chatMessages" class="chat-messages">
                    <div class="message ai-message">
                        👋 Hello! I'm your AI health assistant. You can ask me questions about:
                        <ul style="margin: 0.5rem 0 0 1rem;">
                            <li>Lab result interpretation</li>
                            <li>Supplement recommendations</li>
                            <li>General health questions</li>
                            <li>Symptom analysis</li>
                        </ul>
                        <small><em>⚠️ For educational purposes only. Always consult healthcare professionals for medical advice.</em></small>
                    </div>
                </div>
                
                <div class="input-container">
                    <textarea 
                        id="chatInput" 
                        class="chat-input" 
                        placeholder="Ask about your health, lab results, or symptoms..."
                        rows="2"
                    ></textarea>
                    <button id="sendBtn" class="send-btn">Send</button>
                </div>
            </div>

            <div class="nav-links">
                <a href="/">← Home</a> |
                <a href="/scanner">Document Scanner</a> |
                <a href="/journal">Health Journal</a>
            </div>
        </div>

        <script>
            const chatMessages = document.getElementById('chatMessages');
            const chatInput = document.getElementById('chatInput');
            const sendBtn = document.getElementById('sendBtn');

            function addMessage(message, isUser = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
                messageDiv.innerHTML = message;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function showTyping() {
                const typingDiv = document.createElement('div');
                typingDiv.className = 'typing';
                typingDiv.id = 'typing-indicator';
                typingDiv.textContent = '🤖 AI is thinking...';
                chatMessages.appendChild(typingDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function hideTyping() {
                const typingDiv = document.getElementById('typing-indicator');
                if (typingDiv) {
                    typingDiv.remove();
                }
            }

            async function sendMessage() {
                const message = chatInput.value.trim();
                if (!message) return;

                // Add user message
                addMessage(message, true);
                chatInput.value = '';

                // Show typing indicator
                showTyping();

                try {
                    const response = await fetch('/api/health-analysis', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ question: message })
                    });

                    const result = await response.json();
                    
                    hideTyping();
                    addMessage(result.response || 'Sorry, I could not process your question.');
                    
                } catch (error) {
                    hideTyping();
                    addMessage('Sorry, there was an error processing your question. Please try again.');
                }
            }

            sendBtn.addEventListener('click', sendMessage);

            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

# ===== HEALTH GPT API ENDPOINT =====
@app.post("/api/health-analysis")
async def health_analysis(data: dict):
    """Health GPT analysis endpoint"""
    try:
        question = data.get('question', '')
        
        # Mock AI response - you'll integrate with OpenAI API
        response = generate_health_response(question)
        
        return {"response": response}
        
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

def generate_health_response(question):
    """Generate health response - integrate with OpenAI API"""
    
    # Mock responses based on keywords
    question_lower = question.lower()
    
    if 'vitamin d' in question_lower:
        return """
        **Vitamin D Information:**
        
        # Vitamin D is crucial for bone health, immune function, and overall wellness. Here's what you should know:
        
        • **Optimal levels**: 50 ng/mL 
        • **Low levels**: Can cause fatigue, bone pain, muscle weakness, mood changes
        • **Sources**: Sunlight exposure (15-30 min daily), fatty fish, fortified foods, supplements
        • **Supplementation**: Follow my Vitamin D Protocol, but consult your doctor for personalized dosing
        
        # Always get tested before starting supplementation and work with a healthcare provider.
        """
    
    elif 'lymphocytes' in question_lower or 'neutrophils' in question_lower:
        return """
        **White Blood Cell Information:**
        
        • **Lymphocytes (30%)**: Part of immune system, fight infections and diseases
        • **Neutrophils (60%)**: First responders to bacterial infections
        
        **Abnormal levels may indicate:**
        - High lymphocytes: Viral infections, autoimmune conditions
        - Low lymphocytes: Immunosuppression, stress, certain medications
        - High neutrophils: Bacterial infections, inflammation, stress
        - Low neutrophils: Bone marrow issues, certain medications
        
        Consult your healthcare provider for interpretation of abnormal values.
        """
    
    elif 'supplement' in question_lower:
        return """
        **Supplement Guidance:**
        
        **Before starting any supplements:**
        1. Get tested to identify deficiencies
        2. Consult with healthcare provider
        3. Consider food sources first
        4. Start with quality brands
        5. Monitor for interactions
        
        **Common supplements for health optimization:**
        • Vitamin D3 (if deficient)
        • Omega-3 fatty acids
        • Magnesium
        • B-complex vitamins
        • Probiotics
        
        More is not always better - Listening to your body is key!
        """
    
    else:
        return """
        **Health Assistant Response:**
        
        Thank you for your question! I can help with information about:
        
        • **Lab results interpretation** (Vitamin D, blood counts, etc.)
        • **Supplement recommendations**
        • **General health optimization**
        • **Symptom understanding**
        
        Please ask more specific questions about:
        - Your lab values or symptoms
        - Specific health concerns
        - Supplement questions
        - Lifestyle optimization
        
        For personalized medical advice, always consult with qualified healthcare professionals.
        """
        
@app.get("/test-scanner")
async def test_scanner():
    return {"message": "Scanner route works!", "status": "success"}

@app.get("/simple-test", response_class=HTMLResponse)
async def simple_test():
    return """
    <html>
        <head><title>Simple Test</title></head>
        <body>
            <h1>✅ Simple HTML Test Works!</h1>
            <p>If you see this, your routes are working fine.</p>
        </body>
    </html>
    """
