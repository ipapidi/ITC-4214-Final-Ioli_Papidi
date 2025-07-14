function handleProductCardClick(event, element) {
    // Check if the clicked element or its parent is a button or form
    let target = event.target;
    while (target && target !== element) {
        if (target.tagName === 'BUTTON' || target.tagName === 'A' || target.tagName === 'FORM' || 
            target.classList.contains('btn') || target.classList.contains('non-clickable')) {
            return; // Don't navigate if clicking on interactive elements
        }
        target = target.parentElement;
    }
    // If we get here, it's a safe click on the card
    const productCard = element.closest('.product-card');
    const productUrl = productCard.getAttribute('data-product-url');
    if (productUrl) {
        window.location.href = productUrl;
    }
}

function removeFromWishlist(productId) {
    if (confirm('Are you sure you want to remove this item from your wishlist?')) {
        window.location.href = `/users/wishlist/remove/${productId}/`;
    }
} 