// Vendor Registration Form JavaScript
// This file handles the dynamic behavior of the vendor registration form

document.addEventListener('DOMContentLoaded', function() {
    // Get references to the form elements
<<<<<<< HEAD
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
=======
    const vendorCheckbox = document.getElementById('is_vendor_checkbox'); //Get the vendor checkbox
    const vendorTeamSelect = document.getElementById('vendor_team_select'); //Get the vendor team select
    
    // Check if elements exist before proceeding
    if (!vendorCheckbox || !vendorTeamSelect) { //If the vendor checkbox or vendor team select is not empty
        console.log('Vendor form elements not found'); //Log the vendor form elements not found
        return; //Return
    }
    
    // Function to show/hide the F1 team dropdown
    function toggleVendorTeamDropdown() { 
        // Check if the vendor checkbox is checked
        if (vendorCheckbox.checked) { 
            // Show the dropdown by removing the 'display: none' style
            vendorTeamSelect.style.display = 'block'; 
            // Make the field required when checkbox is checked
            vendorTeamSelect.required = true; 
>>>>>>> a95348d (added comments and meta tags)
        } else {
            // Hide the dropdown
            vendorTeamSelect.style.display = 'none';
            // Clear the selection when hiding
            vendorTeamSelect.value = '';
            // Remove required attribute when checkbox is unchecked
<<<<<<< HEAD
            vendorTeamSelect.required = false;
=======
            vendorTeamSelect.required = false; //Remove the required attribute when checkbox is unchecked
>>>>>>> a95348d (added comments and meta tags)
        }
    }
    
    // Add event listener to the checkbox
    // This will run the toggle function whenever the checkbox is clicked
<<<<<<< HEAD
    vendorCheckbox.addEventListener('change', toggleVendorTeamDropdown);
=======
    vendorCheckbox.addEventListener('change', toggleVendorTeamDropdown); //Add a change event listener to the vendor checkbox
>>>>>>> a95348d (added comments and meta tags)
    
    // Run the function once on page load to set initial state
    // This ensures the dropdown is hidden by default
    toggleVendorTeamDropdown();
}); 