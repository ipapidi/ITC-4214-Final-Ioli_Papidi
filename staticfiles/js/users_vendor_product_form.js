// Vendor Product Form JavaScript
// This file handles file upload validation for the vendor product form

document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
    const imageInput = document.querySelector('input[type="file"]');
    const maxFileSize = 5 * 1024 * 1024; // 5MB in bytes
    const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
    
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Check file size
                if (file.size > maxFileSize) {
                    alert('File size cannot exceed 5MB. Please choose a smaller image.');
=======
    const imageInput = document.querySelector('input[type="file"]'); //Get the image input
    const maxFileSize = 5 * 1024 * 1024; // 5MB in bytes
    const validExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']; //Get the valid extensions
    
    if (imageInput) { //If the image input is not empty
        imageInput.addEventListener('change', function(e) { //Add a change event listener to the image input
            const file = e.target.files[0]; //Get the file
            if (file) { //If the file is not empty
                // Check file size
                if (file.size > maxFileSize) { //If the file size is greater than 5MB
                    alert('File size cannot exceed 5MB. Please choose a smaller image.'); //Alert the user to choose a smaller image
>>>>>>> a95348d (added comments and meta tags)
                    this.value = ''; // Clear the input
                    return;
                }
                
                // Check file extension
<<<<<<< HEAD
                const fileName = file.name.toLowerCase();
                const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
                
                if (!isValidExtension) {
                    alert('Only image files (JPG, PNG, GIF, WebP) are allowed.');
=======
                const fileName = file.name.toLowerCase(); //Get the file name
                const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext)); //Check if the file extension is valid
                
                if (!isValidExtension) { //If the file extension is not valid
                    alert('Only image files (JPG, PNG, GIF, WebP) are allowed.'); //Alert the user to choose a valid image file
>>>>>>> a95348d (added comments and meta tags)
                    this.value = ''; // Clear the input
                    return;
                }
                
                // Show success message
<<<<<<< HEAD
                console.log('File validation passed:', file.name, 'Size:', (file.size / 1024 / 1024).toFixed(2) + 'MB');
=======
                console.log('File validation passed:', file.name, 'Size:', (file.size / 1024 / 1024).toFixed(2) + 'MB'); //Log the file name and size
>>>>>>> a95348d (added comments and meta tags)
            }
        });
    }
    
    // Form validation
<<<<<<< HEAD
    const form = document.querySelector('form[enctype="multipart/form-data"]');
    if (form) {
        form.addEventListener('submit', function(e) {
            const fileInput = this.querySelector('input[type="file"]');
            if (fileInput && fileInput.files.length > 0) {
                const file = fileInput.files[0];
                
                // Double-check file size on form submission
                if (file.size > maxFileSize) {
                    e.preventDefault();
                    alert('File size cannot exceed 5MB. Please choose a smaller image.');
=======
    const form = document.querySelector('form[enctype="multipart/form-data"]'); //Get the form
    if (form) { //If the form is not empty
        form.addEventListener('submit', function(e) { //Add a submit event listener to the form
            const fileInput = this.querySelector('input[type="file"]'); //Get the file input
            if (fileInput && fileInput.files.length > 0) {
                const file = fileInput.files[0]; //Get the file
                
                // Double-check file size on form submission
                if (file.size > maxFileSize) { //If the file size is greater than 5MB
                    e.preventDefault(); //Prevent the default action
                    alert('File size cannot exceed 5MB. Please choose a smaller image.'); //Alert the user to choose a smaller image
>>>>>>> a95348d (added comments and meta tags)
                    return false;
                }
                
                // Double-check file extension on form submission
<<<<<<< HEAD
                const fileName = file.name.toLowerCase();
                const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
                
                if (!isValidExtension) {
                    e.preventDefault();
                    alert('Only image files (JPG, PNG, GIF, WebP) are allowed.');
=======
                const fileName = file.name.toLowerCase(); //Get the file name
                const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext)); //Check if the file extension is valid
                
                if (!isValidExtension) { //If the file extension is not valid
                    e.preventDefault(); //Prevent the default action
                    alert('Only image files (JPG, PNG, GIF, WebP) are allowed.'); //Alert the user to choose a valid image file
>>>>>>> a95348d (added comments and meta tags)
                    return false;
                }
            }
        });
    }

    // Clear Image button logic
<<<<<<< HEAD
    const clearBtn = document.getElementById('clear-image-btn');
    const clearInput = document.getElementById('clear_image');
    const previewDiv = document.getElementById('current-image-preview');
    if (clearBtn && imageInput) {
        clearBtn.addEventListener('click', function() {
            imageInput.value = '';
            if (clearInput) clearInput.value = '1';
            if (previewDiv) previewDiv.style.display = 'none';
=======
    const clearBtn = document.getElementById('clear-image-btn'); //Get the clear image button
    const clearInput = document.getElementById('clear_image'); //Get the clear input
    const previewDiv = document.getElementById('current-image-preview'); //Get the preview div
    if (clearBtn && imageInput) { //If the clear button and image input are not empty
        clearBtn.addEventListener('click', function() { //Add a click event listener to the clear button
            imageInput.value = ''; //Clear the image input
            if (clearInput) clearInput.value = '1'; //Set the clear input to 1
            if (previewDiv) previewDiv.style.display = 'none'; //Set the preview div to none
>>>>>>> a95348d (added comments and meta tags)
        });
    }
}); 