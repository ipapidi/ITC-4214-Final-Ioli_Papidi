// Contact Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize animations and interactions
    initSmoothScrolling(); // Initialize smooth scrolling
    initFormAnimations(); // Initialize form animations
    initFAQAnimations(); // Initialize FAQ animations
    initContactMethodEffects(); // Initialize contact method effects
});

// Smooth Scrolling
function initSmoothScrolling() {
    const scrollLinks = document.querySelectorAll('.scroll-to'); // Get all scroll links
    
    scrollLinks.forEach(link => { // Iterate over all scroll links
        link.addEventListener('click', function(e) { // Add click event listener to each scroll link
            e.preventDefault();
            const targetId = this.getAttribute('href'); // Get the target ID
            const targetElement = document.querySelector(targetId); // Get the target element
            
            if (targetElement) { // If the target element exists
                const offsetTop = targetElement.offsetTop - 80; // Account for fixed navbar
                
                window.scrollTo({ // Scroll to the target element
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Form Animations
function initFormAnimations() {
    const formInputs = document.querySelectorAll('.form-control'); // Get all form inputs
    
    formInputs.forEach(input => { // Iterate over all form inputs
        // Add focus animation
        input.addEventListener('focus', function() { // Add focus event listener to each form input
            this.parentElement.style.transform = 'translateY(-2px)'; // Move the form input up by 2px
        });
        
        input.addEventListener('blur', function() { // Add blur event listener to each form input
            this.parentElement.style.transform = 'translateY(0)'; // Move the form input back to its original position
        });
        
        // Add typing animation
        input.addEventListener('input', function() { // Add input event listener to each form input
            if (this.value.length > 0) { // If the form input has a value
                this.style.borderColor = 'var(--accent-color)'; // Set the border color to the accent color
            } else {
                this.style.borderColor = 'var(--border-color)'; // Set the border color to the border color
            }
        });
    });
    
    // Form submission animation and validation
    const contactForm = document.querySelector('.contact-form'); // Get the contact form
    if (contactForm) { // If the contact form exists
        contactForm.addEventListener('submit', function(e) { // Add submit event listener to the contact form
            // Client-side validation
            const name = this.querySelector('#name').value.trim(); // Get the name value
            const email = this.querySelector('#email').value.trim(); // Get the email value
            const message = this.querySelector('#message').value.trim(); // Get the message value
            
            let isValid = true; // Initialize isValid to true
            let errorMessage = ''; // Initialize errorMessage to an empty string
            
            // Clear previous error messages
            clearFormErrors(); // Clear previous error messages
            
            // Validate name
            if (!name) {
                showFieldError('name', 'Please enter your name.'); // Show an error message for the name field
                isValid = false; // Set isValid to false
            }
            
            // Validate email
            if (!email) {
                showFieldError('email', 'Please enter your email address.'); // Show an error message for the email field
                isValid = false; // Set isValid to false
            } else if (!isValidEmail(email)) {
                showFieldError('email', 'Please enter a valid email address.'); // Show an error message for the email field
                isValid = false; // Set isValid to false
            }
            
            // Validate message
            if (!message) {
                showFieldError('message', 'Please enter your message.'); // Show an error message for the message field
                isValid = false; // Set isValid to false
            } else if (message.length < 10) {
                showFieldError('message', 'Your message must be at least 10 characters long.'); // Show an error message for the message field
                isValid = false; // Set isValid to false
            }
            
            if (!isValid) {
                e.preventDefault(); // Prevent the form from submitting
                return false; // Return false to prevent the form from submitting
            }
            
            // If valid, show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...'; // Set the submit button text to "Sending..."
                submitBtn.disabled = true; // Disable the submit button
            }
        });
    }
}

// FAQ Animations
function initFAQAnimations() {
    const accordionItems = document.querySelectorAll('.accordion-item'); // Get all accordion items
    
    accordionItems.forEach((item, index) => { // Iterate over all accordion items
        item.style.opacity = '0'; // Set the opacity to 0
        item.style.transform = 'translateY(20px)'; // Move the accordion item down by 20px
        item.style.transition = 'opacity 0.6s ease, transform 0.6s ease'; // Set the transition to 0.6 seconds ease
        
        // Stagger animation
        setTimeout(() => { // Set a timeout to animate the accordion item
            item.style.opacity = '1'; // Set the opacity to 1
            item.style.transform = 'translateY(0)'; // Move the accordion item back to its original position
        }, index * 200); // Stagger animation
    });
    
    // Accordion button hover effects
    const accordionButtons = document.querySelectorAll('.accordion-button'); // Get all accordion buttons
    
    accordionButtons.forEach(button => { // Iterate over all accordion buttons
        button.addEventListener('mouseenter', function() { // Add mouse enter event listener to each accordion button
            this.style.transform = 'scale(1.02)'; // Scale the accordion button up by 2%
        });
        
        button.addEventListener('mouseleave', function() { // Add mouse leave event listener to each accordion button
            this.style.transform = 'scale(1)'; // Scale the accordion button back to its original size
        });
    });
}

// Contact Method Effects
function initContactMethodEffects() {
    const contactMethods = document.querySelectorAll('.contact-method'); // Get all contact methods
    
    contactMethods.forEach(method => { // Iterate over all contact methods
        method.addEventListener('mouseenter', function() { // Add mouse enter event listener to each contact method
            const icon = this.querySelector('.method-icon i'); // Get the contact method icon
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(5deg)'; // Scale the contact method icon up by 20% and rotate it by 5 degrees
            }
        });
        
        method.addEventListener('mouseleave', function() { // Add mouse leave event listener to each contact method
            const icon = this.querySelector('.method-icon i'); // Get the contact method icon
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)'; // Scale the contact method icon back to its original size and rotate it back to 0 degrees
            }
        });
    });
}

// Helper functions for form validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Regular expression to validate email
    return emailRegex.test(email); // Return true if the email is valid, false otherwise
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId); // Get the field
    const formGroup = field.closest('.form-group'); // Get the form group
    
    // Remove existing error message
    const existingError = formGroup.querySelector('.error-message'); // Get the existing error message
    if (existingError) {
        existingError.remove(); // Remove the existing error message
    }
    
    // Add error message
    const errorDiv = document.createElement('div'); // Create a new error message div
    errorDiv.className = 'error-message text-danger mt-1'; // Set the class name to error-message text-danger mt-1
    errorDiv.style.fontSize = '0.875rem'; // Set the font size to 0.875rem
    errorDiv.textContent = message; // Set the text content to the error message
    
    formGroup.appendChild(errorDiv);
    
    // Add error styling to field
    field.classList.add('is-invalid'); // Add the is-invalid class to the field
    field.style.borderColor = '#dc3545'; // Set the border color to red
}

function clearFormErrors() {
    // Remove all error messages
    const errorMessages = document.querySelectorAll('.error-message'); // Get all error messages
    errorMessages.forEach(error => error.remove()); // Remove all error messages
    
    // Remove error styling from fields
    const invalidFields = document.querySelectorAll('.is-invalid'); // Get all invalid fields
    invalidFields.forEach(field => { // Iterate over all invalid fields
        field.classList.remove('is-invalid'); // Remove the is-invalid class from the field
        field.style.borderColor = ''; // Set the border color to an empty string
    });
}

// Add CSS for form animations and validation
const style = document.createElement('style'); // Create a new style element
style.textContent = ` 
    .form-group {
        transition: transform 0.3s ease;
    }
    
    .accordion-item {
        transition: all 0.3s ease;
    }
    
    .accordion-button {
        transition: all 0.3s ease;
    }
    
    .method-icon i {
        transition: transform 0.3s ease;
    }
    
    .contact-form button[type="submit"] {
        transition: all 0.3s ease;
    }
    
    .contact-form button[type="submit"]:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }
    
    .error-message {
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .is-invalid {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25) !important;
    }
`;
document.head.appendChild(style); // Append the style element to the head