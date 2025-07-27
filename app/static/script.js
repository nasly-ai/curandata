// This script runs after the entire HTML page is loaded
document.addEventListener('DOMContentLoaded', () => {

    // --- LOGIC FOR THE HOMEPAGE UPLOAD ---
    // (This part remains the same)
    if (document.querySelector('.hero-section')) {
        const dropZone = document.querySelector('.drop-zone');
        const analyzeButton = document.querySelector('.hero-section .btn-primary');
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf, .png, .jpg, .jpeg';
        fileInput.style.display = 'none';

        const handleFileSelect = (file) => {
            if (file) {
                console.log('File selected:', file.name);
                alert(`You have selected the file: ${file.name}. Now we would upload and analyze it.`);
            }
        };

        fileInput.addEventListener('change', (e) => handleFileSelect(e.target.files[0]));
        if (dropZone) {
            dropZone.addEventListener('click', () => fileInput.click());
            dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--accent-color)'; });
            dropZone.addEventListener('dragleave', () => { dropZone.style.borderColor = 'var(--border-color)'; });
            dropZone.addEventListener('drop', (e) => { e.preventDefault(); dropZone.style.borderColor = 'var(--border-color)'; handleFileSelect(e.dataTransfer.files[0]); });
        }
        if (analyzeButton) {
            analyzeButton.addEventListener('click', (e) => { e.preventDefault(); fileInput.click(); });
        }
        document.body.appendChild(fileInput);
    }

    // --- LOGIC FOR THE INTERACTIVE JOURNAL ---
    if (document.querySelector('#journal-section')) {
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
            console.log("Form submitted:", data);
            alert("Entry saved! (Check the browser console for data)");
            closeModal();
        });

        renderCalendar();
    }
});
