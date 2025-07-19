function handleProductCardClick(event, element) { //Function to handle the product card click
    // Check if the clicked element or its parent is a button or form
    let target = event.target; //Get the target
    while (target && target !== element) { //While the target is not the element
        if (target.tagName === 'BUTTON' || target.tagName === 'A' || target.tagName === 'FORM' || 
            target.classList.contains('btn') || target.classList.contains('non-clickable')) { //If the target is a button, a link, a form, or a class contains btn or non-clickable
            return; // Don't navigate if clicking on interactive elements
        }
        target = target.parentElement; //Get the parent element
    }
    // If we get here, it's a safe click on the card
    const productCard = element.closest('.product-card'); //Get the product card
    const productUrl = productCard.getAttribute('data-product-url'); //Get the product url
    if (productUrl) { //If the product url is not empty
        window.location.href = productUrl; //Navigate to the product url
    }
}

function removeFromWishlist(productId) { //Function to remove an item from the wishlist
    if (confirm('Are you sure you want to remove this item from your wishlist?')) { //If the user confirms
        window.location.href = `/users/wishlist/remove/${productId}/`; //Navigate to the wishlist remove url
    }
} 