document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')); //Get all elements with data-bs-toggle="tooltip"
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) { //Map each element to a tooltip
        return new bootstrap.Tooltip(tooltipTriggerEl); //Create a new tooltip
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]')); //Get all elements with data-bs-toggle="popover"
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) { //Map each element to a popover
        return new bootstrap.Popover(popoverTriggerEl); //Create a new popover
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => { //Get all elements with href starting with "#"
        anchor.addEventListener('click', function (e) { //Add a click event listener to each element
            e.preventDefault(); //Prevent the default behavior
            const target = document.querySelector(this.getAttribute('href')); //Get the target element
            if (target) { 
                target.scrollIntoView({ //Scroll to the target element
                    behavior: 'smooth', //Smooth scrolling
                    block: 'start' //Scroll to the start of the target element
                });
            }
        });
    });

    // Simple hover effects for cards
    document.querySelectorAll('.product-card, .category-card').forEach(card => { //Get all elements with class "product-card" or "category-card"
        card.addEventListener('mouseenter', function() { //Add a mouseenter event listener to each element
            this.style.transform = 'translateY(-5px)'; //Move the card up by 5px
        });
        
        card.addEventListener('mouseleave', function() { //Add a mouseleave event listener to each element
            this.style.transform = 'translateY(0)'; //Move the card back to its original position
        });
    });

    // Form validation
    document.querySelectorAll('form').forEach(form => { //Get all forms
        form.addEventListener('submit', function(e) { //Add a submit event listener to each form
            const requiredFields = form.querySelectorAll('[required]'); //Get all required fields
            let isValid = true; //Set the validity to true
            
            requiredFields.forEach(field => { //For each required field
                if (!field.value.trim()) { //If the field is empty
                    isValid = false; //Set the validity to false
                    field.classList.add('is-invalid'); //Add the class "is-invalid" to the field
                } else {
                    field.classList.remove('is-invalid'); //Remove the class "is-invalid" from the field
                }
            });
            
            if (!isValid) {
                e.preventDefault(); //Prevent the default behavior
            }
        });
    });
}); 