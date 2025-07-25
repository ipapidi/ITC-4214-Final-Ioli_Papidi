function toggleWishlist(productId, isInWishlist, btn) {
    const url = isInWishlist //If the product is in the wishlist, remove it, otherwise add it
        ? `/users/wishlist/remove/${productId}/` //If the product is in the wishlist, remove it
        : `/users/wishlist/add/${productId}/`; //If the product is not in the wishlist, add it
    
    const csrfToken = getCSRFToken();
    console.log('Making request to:', url);
    console.log('CSRF Token:', csrfToken);
    
    fetch(url, {
        method: 'POST', //Send a POST request
        headers: {
            'X-CSRFToken': csrfToken, //Get the CSRF token
            'X-Requested-With': 'XMLHttpRequest' //Set the X-Requested-With header to XMLHttpRequest
        }
    })
    .then(response => response.json()) //Parse the response as JSON
    .then(data => {
        if (data.status === 'added') { //If the product is added to the wishlist
            btn.classList.remove('btn-outline-danger'); //Remove the btn-outline-danger class
            btn.classList.add('btn-danger'); //Add the btn-danger class
            btn.innerHTML = '<i class="fas fa-heart"></i>'; //Set the button to a heart icon
            btn.setAttribute('title', 'Remove from Wishlist'); //Set the button title to "Remove from Wishlist"
            btn.setAttribute('onclick', `toggleWishlist(${productId}, true, this)`); //Set the button onclick to toggle the wishlist
        } else if (data.status === 'removed') {
            btn.classList.remove('btn-danger'); //Remove the btn-danger class
            btn.classList.add('btn-outline-danger'); //Add the btn-outline-danger class
            btn.innerHTML = '<i class="far fa-heart"></i>'; //Set the button to a heart icon
            btn.setAttribute('title', 'Add to Wishlist'); //Set the button title to "Add to Wishlist"
            btn.setAttribute('onclick', `toggleWishlist(${productId}, false, this)`); //Set the button onclick to toggle the wishlist
        }
    });
}

function getCookie(name) { //Get the cookie
    let cookieValue = null; //Set the cookie value to null
    if (document.cookie && document.cookie !== '') { //If the cookie is not empty
        const cookies = document.cookie.split(';'); //Split the cookie into an array
        for (let i = 0; i < cookies.length; i++) { //For each cookie
            const cookie = cookies[i].trim(); //Trim the cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) { //If the cookie name is the same as the name
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); //Decode the cookie
                break;
            }
        }
    }
    return cookieValue;
}

function getCSRFToken() {
    // First try to get from meta tag
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
        const token = metaToken.getAttribute('content');
        console.log('CSRF token from meta tag:', token);
        return token;
    }
    
    // Fallback to cookie
    const cookieToken = getCookie('csrftoken');
    console.log('CSRF token from cookie:', cookieToken);
    return cookieToken;
} 
