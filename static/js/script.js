// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Handle search form submission
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            const queryInput = document.getElementById('query-input');
            if (queryInput && queryInput.value.trim() === '') {
                event.preventDefault();
                showAlert('Please enter your movie preferences or a description.', 'warning');
            }
        });
    }

    // Function to show alerts
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        if (alertContainer) {
            const alert = document.createElement('div');
            alert.className = `alert alert-${type} alert-dismissible fade show`;
            alert.role = 'alert';
            alert.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            `;
            
            alertContainer.appendChild(alert);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                alert.classList.remove('show');
                setTimeout(() => {
                    alertContainer.removeChild(alert);
                }, 150);
            }, 5000);
        }
    }

    // Example movies for recommendation inspiration
    const exampleMovies = [
        "A sci-fi adventure with aliens and space travel",
        "A romantic comedy about two people who meet in a bookstore",
        "A thriller with unexpected twists and turns",
        "A historical drama set during World War II",
        "An action movie with car chases and explosions"
    ];

    // Set up example suggestion functionality
    const suggestionsContainer = document.getElementById('example-suggestions');
    const queryInput = document.getElementById('query-input');
    
    if (suggestionsContainer && queryInput) {
        exampleMovies.forEach(example => {
            const button = document.createElement('button');
            button.className = 'btn btn-sm btn-outline-secondary me-2 mb-2';
            button.textContent = example;
            button.addEventListener('click', function() {
                queryInput.value = example;
                queryInput.focus();
            });
            suggestionsContainer.appendChild(button);
        });
    }

    // Animate progress bars on recommendation page
    const progressBars = document.querySelectorAll('.progress-bar');
    if (progressBars.length > 0) {
        progressBars.forEach(bar => {
            const targetWidth = bar.getAttribute('aria-valuenow') + '%';
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.transition = 'width 1s ease-out';
                bar.style.width = targetWidth;
            }, 100);
        });
    }
});
