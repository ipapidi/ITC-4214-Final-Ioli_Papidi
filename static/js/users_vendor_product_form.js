// Vendor Product Form JavaScript
// This file handles file upload validation for the vendor product form

document.addEventListener('DOMContentLoaded', function() {
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
                    this.value = ''; // Clear the input
                    return;
                }
                
                // Check file extension
                const fileName = file.name.toLowerCase();
                const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
                
                if (!isValidExtension) {
                    alert('Only image files (JPG, PNG, GIF, WebP) are allowed.');
                    this.value = ''; // Clear the input
                    return;
                }
                
                // Show success message
                console.log('File validation passed:', file.name, 'Size:', (file.size / 1024 / 1024).toFixed(2) + 'MB');
            }
        });
    }
    
    // Form validation
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
                    return false;
                }
                
                // Double-check file extension on form submission
                const fileName = file.name.toLowerCase();
                const isValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
                
                if (!isValidExtension) {
                    e.preventDefault();
                    alert('Only image files (JPG, PNG, GIF, WebP) are allowed.');
                    return false;
                }
            }
        });
    }

    // Clear Image button logic
    const clearBtn = document.getElementById('clear-image-btn');
    const clearInput = document.getElementById('clear_image');
    const previewDiv = document.getElementById('current-image-preview');
    if (clearBtn && imageInput) {
        clearBtn.addEventListener('click', function() {
            imageInput.value = '';
            if (clearInput) clearInput.value = '1';
            if (previewDiv) previewDiv.style.display = 'none';
        });
    }
}); 