function updateSubcategories() {
<<<<<<< HEAD
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
=======
    const category = document.getElementById('category-select').value; //Get the category
    fetch(`/ajax/subcategories/?category=${encodeURIComponent(category)}`) //Fetch the subcategories
        .then(response => response.json()) //Parse the response as JSON
        .then(data => {
            const subcatSelect = document.getElementById('subcategory-select'); //Get the subcategory select
            subcatSelect.innerHTML = '<option value="">All</option>'; //Set the subcategory select to an empty option
            data.subcategories.forEach(subcat => { //For each subcategory
                const option = document.createElement('option'); //Create an option
                option.value = subcat.slug; //Set the option value to the subcategory slug
                option.textContent = subcat.name; //Set the option text to the subcategory name
                subcatSelect.appendChild(option); //Append the option to the subcategory select
>>>>>>> a95348d (added comments and meta tags)
            });
        });
}

function handleProductCardClick(event, element) {
    // Check if the clicked element or its parent is a button or form
<<<<<<< HEAD
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
=======
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
>>>>>>> a95348d (added comments and meta tags)
    }
}

function addToWishlist(productId) {
<<<<<<< HEAD
    window.location.href = `/users/wishlist/add/${productId}/`;
}

function removeFromWishlist(productId) {
    if (confirm('Are you sure you want to remove this item from your wishlist?')) {
        window.location.href = `/users/wishlist/remove/${productId}/`;
=======
    window.location.href = `/users/wishlist/add/${productId}/`; //Navigate to the wishlist add url
}

function removeFromWishlist(productId) {
    if (confirm('Are you sure you want to remove this item from your wishlist?')) { //If the user confirms
        window.location.href = `/users/wishlist/remove/${productId}/`; //Navigate to the wishlist remove url
>>>>>>> a95348d (added comments and meta tags)
    }
} 