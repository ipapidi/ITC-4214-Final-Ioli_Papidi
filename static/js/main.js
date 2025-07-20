document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')); // Get all tooltip triggers
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) { // Map over all tooltip triggers
        return new bootstrap.Tooltip(tooltipTriggerEl); // Create a new tooltip
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]')); // Get all popover triggers
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) { // Map over all popover triggers
        return new bootstrap.Popover(popoverTriggerEl); // Create a new popover
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => { // Iterate over all anchor links
        anchor.addEventListener('click', function (e) { // Add click event listener to each anchor link
            e.preventDefault(); // Prevent the default behavior
            const target = document.querySelector(this.getAttribute('href')); // Get the target element
            if (target) { // If the target element exists
                target.scrollIntoView({ // Scroll to the target element
                    behavior: 'smooth', // Smooth scrolling
                    block: 'start' // Scroll to the start of the target element
                });
            }
        });
    }); // Scroll to the target element

    // Simple hover effects for cards
    document.querySelectorAll('.product-card, .category-card').forEach(card => { // Iterate over all product and category cards
        card.addEventListener('mouseenter', function() { // Add mouse enter event listener to each card
            this.style.transform = 'translateY(-5px)'; // Move the card up by 5px
        });
        
        card.addEventListener('mouseleave', function() { // Add mouse leave event listener to each card
            this.style.transform = 'translateY(0)'; // Move the card back to its original position
        });
    });

    // Form validation
    document.querySelectorAll('form').forEach(form => { // Iterate over all forms
        form.addEventListener('submit', function(e) { // Add submit event listener to each form
            const requiredFields = form.querySelectorAll('[required]'); // Get all required fields
            let isValid = true; // Initialize isValid to true
            
            requiredFields.forEach(field => { // Iterate over all required fields
                if (!field.value.trim()) { // If the field is empty
                    isValid = false; // Set isValid to false
                    field.classList.add('is-invalid'); // Add is-invalid class to the field
                } else {
                    field.classList.remove('is-invalid'); // Remove is-invalid class from the field
                }
            });
            
            if (!isValid) { // If the form is not valid
                e.preventDefault(); // Prevent the default behavior
            }
        });
    });

    // Simple active page highlighting
    const currentPath = window.location.pathname; // Get the current path
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link'); // Get all navigation links
    
    navLinks.forEach(link => { // Iterate over all navigation links
        if (link.getAttribute('href') === currentPath) { // If the link is the current page
            link.style.background = 'rgba(220, 53, 69, 0.2)'; // Set the background color to rgba(220, 53, 69, 0.2)
            link.style.borderRadius = '4px'; // Set the border radius to 4px
        }
    });
}); 