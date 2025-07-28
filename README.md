# CuraData: AI Health Coach for Biological Analysis

**Final Project: NLP & Computer Vision Course - CAI2840C**  
**Student:** Nasly Duarte | **Institution:** MDC Summer 2025  
**Brand:** Girlgoneverde - Think Like a Healer Initiative

---

## 🔍 Problem Statement

### Primary Problem  
The American workforce suffers from a **$530 billion annual productivity crisis** caused by **undiagnosed cognitive dysfunction** linked to correctable biomarker imbalances. Current healthcare systems treat symptoms with pharmaceuticals rather than addressing root causes.

### Specific Issues Identified  
- **Communication Breakdown**: Inability to articulate ideas clearly  
- **Learning Disabilities**: Cognitive fog affecting skill acquisition  
- **Emotional Dysregulation**: Depression and irritability harming team culture  
- **Memory Impairment**: Forgetfulness reducing accuracy and performance  
- **Career Stagnation**: Poor cognition blocking professional growth

### The Gap in Current Solutions  
- "Normal" lab ranges don't reflect **optimal cognitive health**  
- Workplace wellness focuses on **fitness**, not biomarkers  
- No AI tools exist for **lab-based cognitive optimization**  
- Functional medicine is not **accessible to professionals**

### Business Impact  
Companies unknowingly lose productivity due to correctable deficiencies (e.g., **Vitamin D, cholesterol, immune markers**) that affect cognitive performance.

---

## 🧩 Stakeholder Map

### Primary Stakeholders
- **Corporate HR Departments**  
  Role: Wellness program implementation  
  Interest: Lower costs, boost productivity  
  Influence: **High**

- **Working Professionals (End Users)**  
  Role: Direct users of CuraData  
  Interest: Better performance, improved life quality  
  Influence: **Medium**

- **Functional Medicine Practitioners**  
  Role: Clinical advisors  
  Interest: Spread evidence-based healing  
  Influence: **High**

### Secondary Stakeholders
- **Corporate Executives/C-Suite**  
  Role: Budget and strategy decisions  
  Interest: ROI, optimized workforce  
  Influence: **Very High**

- **Healthcare Insurance Providers**  
  Role: Support cost-effective solutions  
  Interest: Reduced claims  
  Influence: **Medium**

- **IT Departments**  
  Role: Security and integration  
  Interest: Data compliance  
  Influence: **Medium**

### Supporting Stakeholders
- **Academic Institutions**  
  Role: Research and development  
  Influence: **Low**

- **Laboratory Partners**  
  Role: Data integration  
  Influence: **Low**

## Diagram 

<img width="610" height="372" alt="Curandata drawio" src="https://github.com/user-attachments/assets/ab009b46-9f98-401c-a2c4-0b4ad18c455d" />

## 🎯 SMART Goals

### Goal 1: Core Analysis Engine Development
- **Specific**: Extract 5 biomarkers (Vitamin D, Cholesterol, Immune markers, Iron, Glucose)  
- **Measurable**: 95% format compatibility, 90% accuracy  
- **Achievable**: Using Tesseract, spaCy, NLTK  
- **Relevant**: Solves biomarker analysis gap  
- **Time-bound**: Week 8

### Goal 2: Computer Vision Component
- **Specific**: Classify stool samples by Bristol Scale  
- **Measurable**: 85% accuracy across 7 types  
- **Achievable**: Using OpenCV, TensorFlow  
- **Relevant**: Gut health = brain health  
- **Time-bound**: Week 10

### Goal 3: Interactive User Interface
- **Specific**: Build Streamlit chatbot for file uploads  
- **Measurable**: Upload + results in <30 seconds  
- **Achievable**: Using Streamlit framework  
- **Relevant**: Democratizes access to insights  
- **Time-bound**: Week 12

### Goal 4: Business Validation
- **Specific**: Case study-based ROI validation  
- **Measurable**: 3 documented case studies  
- **Achievable**: Based on real user results  
- **Relevant**: Supports corporate adoption  
- **Time-bound**: Week 14 (presentation)

### Goal 5: Technical Documentation
- **Specific**: Document system architecture and APIs  
- **Measurable**: Covers 100% of components  
- **Achievable**: Based on working code  
- **Relevant**: Enables handoff and scaling  
- **Time-bound**: Week 15 (submission)

---

## 🛠️ Tools and Technology to Be Used

### Programming Languages
- **Python**: Core development

### Natural Language Processing (NLP)
- **spaCy**: Biomarker extraction  
- **NLTK**: Preprocessing and tokenization  
- **Tesseract OCR**: PDF lab report conversion

### Computer Vision (CV)
- **OpenCV**: Preprocessing biological samples  
- **TensorFlow**: Stool classification model  
- **PIL**: Image formatting

### Data Processing & Analysis
- **Pandas, NumPy**: Data wrangling  
- **Matplotlib, Seaborn**: Visualizations

### Web Interface & Deployment
- **Streamlit**: User interface  
- **Gradio**: Demo deployment

### Development Environment
- **Google Colab, Jupyter**: Notebook development

### File Processing
- **PyPDF2, Pillow**: PDF and image processing

### Database & Storage
- **SQLite**: Local user data  
- **JSON**: Configuration and API responses

### Version Control
- **Git, GitHub**: Versioning and collaboration

### Future Integration
- **FastAPI**: API for enterprise deployment  
- **Docker**: Scalable containerization

---

## 🛠️ Tech Stack
```
| Category            | Tools / Libraries                           |
|---------------------|---------------------------------------------|
| Programming         | Python                                      |
| NLP                 | Tesseract, spaCy, NLTK                      |
| Computer Vision     | OpenCV, TensorFlow, PIL                     |
| Data Analysis       | Pandas, NumPy, Matplotlib, Seaborn          |
| UI / Deployment     | Streamlit, Firebase, Render,                |
| Storage/Auth        | Firebase Firestore & Auth                   |
| Version Control     | Git, GitHub                                 |
| Future Integration  | FastAPI, Docker                             |
```
---

``` your code ```
## 📁 Repository Structure
```
curadata/
├── .gitignore # Ignore Python/cache files
├── README.md # Project overview and setup
├── LICENSE # License for reuse
├── requirements.txt # List of Python dependencies
├── planner.md # Task tracker and project planner
│
├── notebooks/ # Development and analysis notebooks
│ ├── lab_parser.ipynb # NLP-based biomarker extraction
│ ├── stool_classifier.ipynb # CV model for Bristol Stool classification
│ └── exploratory_analysis.ipynb # Initial exploration
│
├── ui/ # Streamlit app interface
│ └── app.py # Main Streamlit UI file
│
├── src/ # Core backend Python modules
│ ├── ocr_utils.py # OCR using Tesseract
│ ├── nlp_utils.py # NLP parsing logic
│ ├── cv_utils.py # CV preprocessing and classification
│ └── health_engine.py # ABCDE supplement recommendation logic
│
├── data/ # Sample data files
│ ├── samples/ # Example PDFs, images
│ └── datasets/ # Optional stool or biomarker datasets
│
├── assets/ # Visual assets for docs and UI
│ ├── architecture.png # Architecture diagram
│ └── slide_assets/ # Icons and images for slide deck
│
├── docs/ # Technical and user documentation
│ ├── executive_summary.md # Summary for stakeholders
│ ├── architecture.md # System architecture explanation
│ └── user_guide.md # Instructions for users
│
├── tests/ # Unit and integration tests
│ └── test_lab_parser.py # Test cases for lab parsing functions
│
└── .streamlit/ # Streamlit app configuration
└── config.toml # Theme and layout settings
```


---

## ✅ Success Metrics

- **Technical**: 90%+ biomarker accuracy  
- **User Experience**: <30s feedback loop  
- **Business**: Case studies showing improved performance  
- **Academic**: Demonstrates NLP + CV integration  
- **Innovation**: Merges AI with functional medicine

---

> _"From Accountant to Healer: Scaling Personal Health Transformation Through AI"_  
**Mission:** Democratize cognitive health optimization for working professionals using functional medicine and AI.


