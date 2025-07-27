// This script runs after the entire HTML page is loaded
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. UPLOAD AND PDF PROCESSING LOGIC (CLIENT-SIDE) ---
    const dropZone = document.querySelector('.drop-zone');
    if (dropZone) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf'; // We are now handling PDFs specifically
        fileInput.style.display = 'none';

        const dropZoneText = dropZone.querySelector('p');
        const originalDropZoneText = dropZoneText.textContent;
        const resultsDisplay = document.getElementById('results-display');

        // This is the new function that processes the file in the browser
        const processPdf = async (file) => {
            if (!file || file.type !== 'application/pdf') {
                alert('Please select a PDF file.');
                return;
            }

            // Give user feedback
            dropZoneText.textContent = 'Reading PDF...';
            resultsDisplay.style.display = 'none'; // Hide old results

            const reader = new FileReader();
            reader.readAsArrayBuffer(file);

            reader.onload = async (event) => {
                try {
                    dropZoneText.textContent = 'Processing...';
                    const pdf = await pdfjsLib.getDocument(event.target.result).promise;
                    let fullText = '';

                    // Loop through all pages of the PDF
                    for (let i = 1; i <= pdf.numPages; i++) {
                        const page = await pdf.getPage(i);
                        const textContent = await page.getTextContent();
                        const pageText = textContent.items.map(item => item.str).join(' ');
                        fullText += pageText + '\n\n'; // Add space between pages
                    }

                    // Display the results
                    resultsDisplay.innerHTML = `<h3>Results for ${file.name}</h3><pre>${fullText.trim()}</pre>`;
                    resultsDisplay.style.display = 'block';
                    dropZoneText.textContent = 'Success! Upload another file.';

                } catch (error) {
                    console.error('Error processing PDF:', error);
                    resultsDisplay.innerHTML = `<h3 style="color: red;">Error</h3><p>Could not read this PDF. It may be corrupted or an image-only PDF.</p>`;
                    resultsDisplay.style.display = 'block';
                    dropZoneText.textContent = 'Processing failed. Please try again.';
                } finally {
                    // Reset the drop zone text after a few seconds
                    setTimeout(() => {
                        dropZoneText.textContent = originalDropZoneText;
                    }, 5000);
                }
            };
        };

        // --- Event listeners to trigger the processing ---
        fileInput.addEventListener('change', (e) => processPdf(e.target.files[0]));
        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--accent-color)'; });
        dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = 'var(--border-color)'; });
        dropZone.addEventListener('drop', (e) => { e.preventDefault(); processPdf(e.dataTransfer.files[0]); });
        document.body.appendChild(fileInput);
    }

document.addEventListener('DOMContentLoaded', () => {

    // --- 1. UPLOAD SECTION LOGIC ---
    const dropZone = document.querySelector('.drop-zone');
    if (dropZone) {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf, .png, .jpg, .jpeg';
        fileInput.style.display = 'none';

        const handleFileSelect = (file) => {
            if (file) {
                console.log('File selected:', file.name);
                alert(`You have selected the file: ${file.name}. Uploading and analyzing...`);
            }
        };

        fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));
        dropZone.addEventListener('click', () => fileInput.click());
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--accent-color)'; });
        dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = 'var(--border-color)'; });
        dropZone.addEventListener('drop', (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--border-color)'; handleFileSelect(e.dataTransfer.files[0]); });
        document.body.appendChild(fileInput);
    }

    // --- 2. INTERACTIVE JOURNAL & MODAL LOGIC ---
    const journalSection = document.querySelector('#journal-section');
    if (journalSection) {
        const monthYearElement = document.getElementById('current-month-year');
        const calendarGrid = document.getElementById('calendar-grid');
        const prevBtn = document.getElementById('prev-month-btn');
        const nextBtn = document.getElementById('next-month-btn');
        const modal = document.getElementById('entryModal');
        const modalDate = document.getElementById('selectedDate');
        const cancelBtn = document.getElementById('cancelBtn');
        const entryForm = document.getElementById('entryForm');

        let currentDate = new Date();
        
        const openModal = (date) => {
            modalDate.textContent = new Date(date + 'T00:00:00').toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
            entryForm.reset();
            modal.classList.remove('hidden');
        };

        const closeModal = () => {
            modal.classList.add('hidden');
        };

        const renderCalendar = () => {
            const year = currentDate.getFullYear();
            const month = currentDate.getMonth();

            monthYearElement.textContent = new Intl.DateTimeFormat('en-US', { year: 'numeric', month: 'long' }).format(currentDate);
            calendarGrid.innerHTML = '';

            const firstDayOfMonth = new Date(year, month, 1).getDay();
            const lastDateOfMonth = new Date(year, month + 1, 0).getDate();

            for (let i = 0; i < firstDayOfMonth; i++) {
                calendarGrid.insertAdjacentHTML('beforeend', '<div class="calendar-day empty"></div>');
            }

            for (let day = 1; day <= lastDateOfMonth; day++) {
                const dayElement = document.createElement('div');
                dayElement.className = 'calendar-day';
                dayElement.textContent = day;
                const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
                
                dayElement.addEventListener('click', () => openModal(dateStr));

                const today = new Date();
                if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                    dayElement.classList.add('today');
                }
                
                calendarGrid.appendChild(dayElement);
            }
        };

        prevBtn.addEventListener('click', () => { currentDate.setMonth(currentDate.getMonth() - 1); renderCalendar(); });
        nextBtn.addEventListener('click', () => { currentDate.setMonth(currentDate.getMonth() + 1); renderCalendar(); });
        cancelBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

        entryForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            console.log("Journal Entry Saved:", data);
            alert("Entry saved! (Check browser console for data)");
            closeModal();
        });

        renderCalendar();
    }
    
    // --- 3. HEALTH ASSISTANT FORM LOGIC ---
    const chatForm = document.querySelector('.chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const chatInput = document.getElementById('chat-input');
            const userQuery = chatInput.value;

            if (userQuery) {
                console.log('User searched for:', userQuery);
                alert(`Searching for: "${userQuery}"...`);
                chatInput.value = '';
            } else {
                alert('Please enter a medicine or question.');
            }
        });
    }
});
