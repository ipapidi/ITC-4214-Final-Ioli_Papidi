// Vendor Registration Form JavaScript
// This file handles the dynamic behavior of the vendor registration form

document.addEventListener('DOMContentLoaded', function() {
    // Get references to the form elements
    const vendorCheckbox = document.getElementById('is_vendor_checkbox');
    const vendorTeamSelect = document.getElementById('vendor_team_select');
    
    // Check if elements exist before proceeding
    if (!vendorCheckbox || !vendorTeamSelect) {
        console.log('Vendor form elements not found');
        return;
    }
    
    // Function to show/hide the F1 team dropdown
    function toggleVendorTeamDropdown() {
        // Check if the vendor checkbox is checked
        if (vendorCheckbox.checked) {
            // Show the dropdown by removing the 'display: none' style
            vendorTeamSelect.style.display = 'block';
            // Make the field required when checkbox is checked
            vendorTeamSelect.required = true;
        } else {
            // Hide the dropdown
            vendorTeamSelect.style.display = 'none';
            // Clear the selection when hiding
            vendorTeamSelect.value = '';
            // Remove required attribute when checkbox is unchecked
            vendorTeamSelect.required = false;
        }
    }
    
    // Add event listener to the checkbox
    // This will run the toggle function whenever the checkbox is clicked
    vendorCheckbox.addEventListener('change', toggleVendorTeamDropdown);
    
    // Run the function once on page load to set initial state
    // This ensures the dropdown is hidden by default
    toggleVendorTeamDropdown();
}); 