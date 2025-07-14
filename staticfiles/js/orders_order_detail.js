function openSupportModal() {
    document.getElementById('supportModal').style.display = 'flex';
}
function closeSupportModal() {
    document.getElementById('supportModal').style.display = 'none';
}
// Optional: Close modal on background click
window.addEventListener('click', function(event) {
    var modal = document.getElementById('supportModal');
    if (event.target === modal) {
        closeSupportModal();
    }
}); 