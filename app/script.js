// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

let selectedFile = null;

// Initialize upload functionality
document.addEventListener('DOMContentLoaded', function() {
    if (uploadArea && fileInput) {
        initializeUpload();
    }
    
    if (window.location.pathname === '/results') {
        initializeResults();
    }
});

function initializeUpload() {
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeDocument);
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processSelectedFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processSelectedFile(files[0]);
    }
}

function processSelectedFile(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png'];
    if (!allowedTypes.includes(file.type)) {
        alert('Please select a PDF, JPG, or PNG file.');
        return;
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        alert('File size must be less than 10MB.');
        return;
    }

    selectedFile = file;
    
    // Update UI
    uploadArea.innerHTML = `
        <div class="upload-icon">
            <i class="fas fa-file-${getFileIcon(file.type)}"></i>
        </div>
        <h3>${file.name}</h3>
        <p>File ready for analysis</p>
        <div class="file-types">
            <span>Size: ${formatFileSize(file.size)}</span>
        </div>
    `;
    
    analyzeBtn.disabled = false;
}

function getFileIcon(fileType) {
    if (fileType === 'application/pdf') return 'pdf';
    if (fileType.startsWith('image/')) return 'image';
    return 'alt';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

async function analyzeDocument() {
    if (!selectedFile) {
        alert('Please select a file first.');
        return;
    }

    // Show progress
    uploadProgress.style.display = 'block';
    analyzeBtn.disabled = true;
    
    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', selectedFile);

        // Update progress
        updateProgress(20, 'Uploading document...');

        // Upload to your API
        const response = await fetch('/api/upload-advanced', {
            method: 'POST',
            body: formData
        });

        updateProgress(50, 'Processing document...');

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const result = await response.json();
        updateProgress(80, 'Analyzing content...');

        // Simulate AI analysis (replace with actual API call)
        await simulateAnalysis(result);
        
        updateProgress(100, 'Analysis complete!');
        
        // Redirect to results page with data
        localStorage.setItem('analysisResult', JSON.stringify({
            filename: selectedFile.name,
            text: result.text,
            analysis: result.analysis || await generateMockAnalysis(result.text),
            timestamp: new Date().toISOString()
        }));
        
        setTimeout(() => {
            window.location.href = '/results';
        }, 1000);

    } catch (error) {
        console.error('Analysis failed:', error);
        alert('Analysis failed. Please try again.');
        uploadProgress.style.display = 'none';
        analyzeBtn.disabled = false;
    }
}

function updateProgress(percentage, text) {
    progressFill.style.width = percentage + '%';
    progressText.textContent = text;
}

async function simulateAnalysis(result) {
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000));
    return result;
}

async function generateMockAnalysis(extractedText) {
    // This would normally call your AI analysis API
    // For now, return a mock analysis
    return {
        summary: "This appears to be a medical report. The document contains test results and medical observations that should be reviewed with your healthcare provider.",
        keyFindings: [
            "Test results are within normal ranges",
            "No immediate concerns identified",
            "Follow-up recommended in 6 months"
        ],
        recommendations: [
            "Discuss these results with your doctor",
            "Maintain current medication regimen",
            "Schedule follow-up appointment"
        ]
    };
}

// Results page functionality
function initializeResults() {
    const analysisData = localStorage.getItem('analysisResult');
    
    if (!analysisData) {
        // No analysis data, redirect to home
        window.location.href = '/';
        return;
    }

    const data = JSON.parse(analysisData);
    displayResults(data);
}

function displayResults(data) {
    // Update document preview
    const documentPreview = document.getElementById('documentPreview');
    if (documentPreview) {
        documentPreview.innerHTML = `
            <div class="document-info">
                <h4><i class="fas fa-file"></i> ${data.filename}</h4>
                <p><strong>Analyzed:</strong> ${formatTimestamp(data.timestamp)}</p>
                <div class="extracted-text">
                    <h5>Extracted Text Preview:</h5>
                    <p>${data.text.substring(0, 200)}...</p>
                </div>
            </div>
        `;
    }

    // Hide loading spinner and show analysis
    const loadingSpinner = document.querySelector('.loading-spinner');
    const analysisContent = document.getElementById('analysisContent');
    
    if (loadingSpinner) loadingSpinner.style.display = 'none';
    
    if (analysisContent && data.analysis) {
        analysisContent.innerHTML = `
            <div class="analysis-summary">
                <p>${data.analysis.summary}</p>
            </div>
        `;
        
        // Show key findings
        const keyFindings = document.getElementById('keyFindings');
        const findingsList = document.getElementById('findingsList');
        
        if (keyFindings && findingsList && data.analysis.keyFindings) {
            keyFindings.style.display = 'block';
            findingsList.innerHTML = data.analysis.keyFindings
                .map(finding => `<div class="finding-item"><i class="fas fa-check-circle"></i> ${finding}</div>`)
                .join('');
        }
        
        // Show recommendations
        const recommendations = document.getElementById('recommendations');
        const recommendationsContent = document.getElementById('recommendationsContent');
        
        if (recommendations && recommendationsContent && data.analysis.recommendations) {
            recommendations.style.display = 'block';
            recommendationsContent.innerHTML = data.analysis.recommendations
                .map(rec => `<div class="recommendation-item"><i class="fas fa-lightbulb"></i> ${rec}</div>`)
                .join('');
        }
    }
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Action button handlers
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('share-btn')) {
        shareResults();
    } else if (event.target.classList.contains('download-btn')) {
        downloadReport();
    } else if (event.target.classList.contains('email-btn')) {
        emailToDoctor();
    }
});

function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'CuraData Analysis Results',
            text: 'Check out my medical report analysis from CuraData',
            url: window.location.href
        });
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href).then(() => {
            alert('Results link copied to clipboard!');
        });
    }
}

function downloadReport() {
    const analysisData = localStorage.getItem('analysisResult');
    if (!analysisData) return;
    
    const data = JSON.parse(analysisData);
    const reportContent = generateReportContent(data);
    
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `curadata-analysis-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function emailToDoctor() {
    const analysisData = localStorage.getItem('analysisResult');
    if (!analysisData) return;
    
    const data = JSON.parse(analysisData);
    const subject = encodeURIComponent('Medical Report Analysis - CuraData');
    const body = encodeURIComponent(generateEmailContent(data));
    
    window.location.href = `mailto:?subject=${subject}&body=${body}`;
}

function generateReportContent(data) {
    return `
CuraData Analysis Report
========================

Document: ${data.filename}
Analyzed: ${formatTimestamp(data.timestamp)}

SUMMARY:
${data.analysis.summary}

KEY FINDINGS:
${data.analysis.keyFindings.map((finding, index) => `${index + 1}. ${finding}`).join('\n')}

RECOMMENDATIONS:
${data.analysis.recommendations.map((rec, index) => `${index + 1}. ${rec}`).join('\n')}

DISCLAIMER:
This analysis is for informational purposes only and should not replace professional medical advice. Always consult with your healthcare provider for medical decisions.

Generated by CuraData - https://curadata.onrender.com
    `.trim();
}

function generateEmailContent(data) {
    return `
Hello Doctor,

I've had my medical report analyzed using CuraData. Here's a summary:

Document: ${data.filename}
Analysis Date: ${formatTimestamp(data.timestamp)}

Summary: ${data.analysis.summary}

I'd like to discuss these results during our next appointment.

Best regards
    `.trim();
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});
