document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
    const stars = document.querySelectorAll('#star-rating .star');
    const ratingInput = document.querySelector('input[name="rating"]');
    let selected = parseInt(ratingInput.value) || 0;

    function fillStars(upto) {
        stars.forEach((star, idx) => {
            if (idx < upto) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled');
=======
    const stars = document.querySelectorAll('#star-rating .star'); //Get all stars
    const ratingInput = document.querySelector('input[name="rating"]'); //Get the rating input
    let selected = parseInt(ratingInput.value) || 0; //Get the selected rating

    function fillStars(upto) { //Fill the stars
        stars.forEach((star, idx) => { //For each star
            if (idx < upto) { //If the index is less than the upto
                star.classList.add('filled'); //Add the filled class to the star
            } else {
                star.classList.remove('filled'); //Remove the filled class from the star
>>>>>>> a95348d (added comments and meta tags)
            }
        });
    }

    stars.forEach((star, idx) => {
<<<<<<< HEAD
        star.addEventListener('mouseenter', function() {
            fillStars(idx + 1);
        });
        star.addEventListener('mouseleave', function() {
            fillStars(selected);
        });
        star.addEventListener('click', function() {
            selected = idx + 1;
            ratingInput.value = selected;
            fillStars(selected);
=======
        star.addEventListener('mouseenter', function() { //Add a mouseenter event listener to the star
            fillStars(idx + 1); //Fill the stars
        });
        star.addEventListener('mouseleave', function() { //Add a mouseleave event listener to the star
            fillStars(selected); //Fill the stars
        });
        star.addEventListener('click', function() { //Add a click event listener to the star
            selected = idx + 1; //Set the selected rating
            ratingInput.value = selected; //Set the rating input value
            fillStars(selected); //Fill the stars
>>>>>>> a95348d (added comments and meta tags)
        });
    });

    // On page load, fill stars if user has a rating
    fillStars(selected);
});

function toggleWishlist(productId, isInWishlist, btn) {
<<<<<<< HEAD
    const url = isInWishlist
        ? `/users/wishlist/remove/${productId}/`
        : `/users/wishlist/add/${productId}/`;
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'added') {
            btn.classList.remove('btn-outline-danger');
            btn.classList.add('btn-danger');
            btn.innerHTML = '<i class="fas fa-heart"></i>';
            btn.setAttribute('title', 'Remove from Wishlist');
            btn.setAttribute('onclick', `toggleWishlist(${productId}, true, this)`);
        } else if (data.status === 'removed') {
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-danger');
            btn.innerHTML = '<i class="far fa-heart"></i>';
            btn.setAttribute('title', 'Add to Wishlist');
=======
    const url = isInWishlist //If the product is in the wishlist, remove it, otherwise add it
        ? `/users/wishlist/remove/${productId}/` //If the product is in the wishlist, remove it
        : `/users/wishlist/add/${productId}/`; //If the product is not in the wishlist, add it
    fetch(url, {
        method: 'POST', //Send a POST request
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), //Get the CSRF token
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
>>>>>>> a95348d (added comments and meta tags)
            btn.setAttribute('onclick', `toggleWishlist(${productId}, false, this)`);
        }
    });
}

<<<<<<< HEAD
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
=======
function getCookie(name) { //Get the cookie
    let cookieValue = null; //Set the cookie value to null
    if (document.cookie && document.cookie !== '') { //If the cookie is not empty
        const cookies = document.cookie.split(';'); //Split the cookie into an array
        for (let i = 0; i < cookies.length; i++) { //For each cookie
            const cookie = cookies[i].trim(); //Trim the cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) { //If the cookie name is the same as the name
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); //Decode the cookie
>>>>>>> a95348d (added comments and meta tags)
                break;
            }
        }
    }
    return cookieValue;
}

<<<<<<< HEAD
function setRecentlyViewed(productId) {
    let viewed = JSON.parse(localStorage.getItem('recently_viewed') || '[]');
    viewed = viewed.filter(id => id !== productId);
    viewed.unshift(productId);
    viewed = viewed.slice(0, 4); // Keep 4 to allow for exclusion
    localStorage.setItem('recently_viewed', JSON.stringify(viewed));
}

function fetchRecentlyViewed(currentProductId) {
    let viewed = JSON.parse(localStorage.getItem('recently_viewed') || '[]');
    viewed = viewed.filter(id => id !== currentProductId);
    viewed = viewed.slice(0, 3);
    console.log('Recently viewed IDs to fetch:', viewed);
    
    if (viewed.length > 0) {
        const container = document.getElementById('recently-viewed-container');
        const recentlyViewedUrl = container.getAttribute('data-recently-viewed-url');
        const csrfToken = container.getAttribute('data-csrf-token');
        
        console.log('Fetching from URL:', recentlyViewedUrl);
        console.log('With CSRF token:', csrfToken);
        console.log('Sending data:', { viewed: viewed });
        
        fetch(recentlyViewedUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ viewed: viewed })
        })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
=======
function setRecentlyViewed(productId) { //Set the recently viewed items
    let viewed = JSON.parse(localStorage.getItem('recently_viewed') || '[]'); //Get the recently viewed items
    viewed = viewed.filter(id => id !== productId); //Filter out the product id
    viewed.unshift(productId); //Add the product id to the beginning of the array
    viewed = viewed.slice(0, 4); // Keep 4 to allow for exclusion
    localStorage.setItem('recently_viewed', JSON.stringify(viewed)); //Set the recently viewed items
}

function fetchRecentlyViewed(currentProductId) { //Fetch the recently viewed items
    let viewed = JSON.parse(localStorage.getItem('recently_viewed') || '[]'); //Get the recently viewed items
    viewed = viewed.filter(id => id !== currentProductId); //Filter out the product id
    viewed = viewed.slice(0, 3); //Keep 3 to allow for exclusion
    console.log('Recently viewed IDs to fetch:', viewed);
    
    if (viewed.length > 0) { //If the viewed array is not empty
        const container = document.getElementById('recently-viewed-container'); //Get the recently viewed container
        const recentlyViewedUrl = container.getAttribute('data-recently-viewed-url'); //Get the recently viewed url
        const csrfToken = container.getAttribute('data-csrf-token'); //Get the CSRF token
        
        console.log('Fetching from URL:', recentlyViewedUrl); //Log the recently viewed url
        console.log('With CSRF token:', csrfToken); //Log the CSRF token
        console.log('Sending data:', { viewed: viewed }); //Log the viewed array
        
        fetch(recentlyViewedUrl, {
            method: "POST", //Send a POST request
            headers: {
                "Content-Type": "application/json", //Set the content type to application/json
                "X-CSRFToken": csrfToken //Set the CSRF token
            },
            body: JSON.stringify({ viewed: viewed }) //Set the body to the viewed array
        })
        .then(response => {
            console.log('Response status:', response.status); //Log the response status
            return response.json(); //Parse the response as JSON
        })
        .then(data => {
            console.log('Response data:', data); //Log the response data
>>>>>>> a95348d (added comments and meta tags)
            if (data.products_html) {
                container.innerHTML = data.products_html;
            }
        })
        .catch(error => {
<<<<<<< HEAD
            console.error('Error fetching recently viewed:', error);
        });
    } else {
        document.getElementById('recently-viewed-container').innerHTML = '';
=======
            console.error('Error fetching recently viewed:', error); //Log the error
        });
    } else {
        document.getElementById('recently-viewed-container').innerHTML = ''; //Set the recently viewed container to an empty string
>>>>>>> a95348d (added comments and meta tags)
    }
}

// Get product ID from data attribute and initialize recently viewed functionality
document.addEventListener('DOMContentLoaded', function() {
<<<<<<< HEAD
    const container = document.getElementById('recently-viewed-container');
    console.log('Container found:', container);
    if (container) {
        const productId = container.getAttribute('data-product-id');
        const recentlyViewedUrl = container.getAttribute('data-recently-viewed-url');
        const csrfToken = container.getAttribute('data-csrf-token');
        
        console.log('Product ID:', productId);
        console.log('Recently viewed URL:', recentlyViewedUrl);
        console.log('CSRF Token:', csrfToken);
        
        if (productId) {
            setRecentlyViewed(productId);
            fetchRecentlyViewed(productId);
=======
    const container = document.getElementById('recently-viewed-container'); //Get the recently viewed container
    console.log('Container found:', container); //Log the container
    if (container) { //If the container is not empty
        const productId = container.getAttribute('data-product-id'); //Get the product id
        const recentlyViewedUrl = container.getAttribute('data-recently-viewed-url'); //Get the recently viewed url
        const csrfToken = container.getAttribute('data-csrf-token'); //Get the CSRF token
        
        console.log('Product ID:', productId); //Log the product id
        console.log('Recently viewed URL:', recentlyViewedUrl); //Log the recently viewed url
        console.log('CSRF Token:', csrfToken); //Log the CSRF token
        
        if (productId) { //If the product id is not empty
            setRecentlyViewed(productId); //Set the recently viewed items
            fetchRecentlyViewed(productId); //Fetch the recently viewed items
>>>>>>> a95348d (added comments and meta tags)
        }
    }
}); 