    // --- LOGIC FOR HEALTH CHAT FORM ---
    const chatForm = document.querySelector('.chat-form');
    if (chatForm) {
        chatForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent the page from reloading
            const chatInput = document.getElementById('chat-input');
            const userQuery = chatInput.value;

            if (userQuery) {
                console.log('User searched for:', userQuery);
                alert(`Searching for: "${userQuery}"... (Functionality to show results would go here)`);
                chatInput.value = ''; // Clear the input field
            } else {
                alert('Please enter a supplement or question.');
            }
        });
    }
