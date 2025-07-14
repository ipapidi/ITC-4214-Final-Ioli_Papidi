function updateSubcategories() {
    const category = document.getElementById('category-select').value;
    fetch(`/ajax/subcategories/?category=${encodeURIComponent(category)}`)
        .then(response => response.json())
        .then(data => {
            const subcatSelect = document.getElementById('subcategory-select');
            subcatSelect.innerHTML = '<option value="">All</option>';
            data.subcategories.forEach(subcat => {
                const option = document.createElement('option');
                option.value = subcat.slug;
                option.textContent = subcat.name;
                subcatSelect.appendChild(option);
            });
        });
}

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

function addToWishlist(productId) {
    window.location.href = `/users/wishlist/add/${productId}/`;
}

function removeFromWishlist(productId) {
    if (confirm('Are you sure you want to remove this item from your wishlist?')) {
        window.location.href = `/users/wishlist/remove/${productId}/`;
    }
} 