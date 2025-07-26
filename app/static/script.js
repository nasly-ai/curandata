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
