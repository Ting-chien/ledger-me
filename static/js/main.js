// Main JavaScript file for LedgerMe

document.addEventListener('DOMContentLoaded', function() {
    console.log('LedgerMe is ready!');
    
    // Add active class to current nav link
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = '#3498db';
        }
    });
});
