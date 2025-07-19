document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap components
<<<<<<< HEAD
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
=======
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
>>>>>>> a95348d (added comments and meta tags)
                });
            }
        });
    });

    // Simple hover effects for cards
<<<<<<< HEAD
    document.querySelectorAll('.product-card, .category-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
=======
    document.querySelectorAll('.product-card, .category-card').forEach(card => { //Get all elements with class "product-card" or "category-card"
        card.addEventListener('mouseenter', function() { //Add a mouseenter event listener to each element
            this.style.transform = 'translateY(-5px)'; //Move the card up by 5px
        });
        
        card.addEventListener('mouseleave', function() { //Add a mouseleave event listener to each element
            this.style.transform = 'translateY(0)'; //Move the card back to its original position
>>>>>>> a95348d (added comments and meta tags)
        });
    });

    // Form validation
<<<<<<< HEAD
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
=======
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
>>>>>>> a95348d (added comments and meta tags)
                }
            });
            
            if (!isValid) {
<<<<<<< HEAD
                e.preventDefault();
=======
                e.preventDefault(); //Prevent the default behavior
>>>>>>> a95348d (added comments and meta tags)
            }
        });
    });
}); 