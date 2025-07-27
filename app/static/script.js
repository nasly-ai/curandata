// This script runs after the entire HTML page is loaded
document.addEventListener('DOMContentLoaded', () => {

    // Find the elements we need to interact with on the homepage
    const dropZone = document.querySelector('.drop-zone');
    const analyzeButton = document.querySelector('.hero-section .btn-primary');
    
    // Create a hidden file input to handle the actual file selection
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.pdf, .png, .jpg, .jpeg';
    fileInput.style.display = 'none';

    // This function will be called when a file is selected
    const handleFileSelect = (file) => {
        if (file) {
            console.log('File selected:', file.name);
            alert(`You have selected the file: ${file.name}. Now we would upload and analyze it.`);
            // In a real application, you would start the upload process here.
            // For example: uploadAndAnalyze(file);
        }
    };

    // When the user selects a file through the hidden input, handle it
    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // If the user clicks the drop zone, trigger the hidden file input
    if (dropZone) {
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Add visual feedback when a file is dragged over the drop zone
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault(); // This is necessary to allow dropping
            dropZone.style.borderColor = 'var(--accent-color)';
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.style.borderColor = 'var(--border-color)';
        });

        // Handle the file when it is dropped
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault(); // Prevent the browser from opening the file
            dropZone.style.borderColor = 'var(--border-color)';
            handleFileSelect(e.dataTransfer.files[0]);
        });
    }

    // If the user clicks the "Analyze Document" button, also trigger the file input
    if (analyzeButton) {
        analyzeButton.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent the link from navigating
            fileInput.click();
        });
    }
    
    // Append the hidden file input to the document so it's usable
    document.body.appendChild(fileInput);
});
