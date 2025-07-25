function openSupportModal() {
    document.getElementById('supportModal').style.display = 'flex'; //Show the support modal
}
function closeSupportModal() {
    document.getElementById('supportModal').style.display = 'none'; //Hide the support modal
}
// Optional: Close modal on background click
window.addEventListener('click', function(event) {
    var modal = document.getElementById('supportModal'); //Get the support modal
    if (event.target === modal) { //If the target is the support modal
        closeSupportModal(); //Close the support modal
    }
}); 