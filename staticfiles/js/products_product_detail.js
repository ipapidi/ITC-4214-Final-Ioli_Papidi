document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('#star-rating .star');
    const ratingInput = document.querySelector('input[name="rating"]');
    let selected = parseInt(ratingInput.value) || 0;

    function fillStars(upto) {
        stars.forEach((star, idx) => {
            if (idx < upto) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled');
            }
        });
    }

    stars.forEach((star, idx) => {
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
        });
    });

    // On page load, fill stars if user has a rating
    fillStars(selected);
});

function toggleWishlist(productId, isInWishlist, btn) {
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
            btn.setAttribute('onclick', `toggleWishlist(${productId}, false, this)`);
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
            if (data.products_html) {
                container.innerHTML = data.products_html;
            }
        })
        .catch(error => {
            console.error('Error fetching recently viewed:', error);
        });
    } else {
        document.getElementById('recently-viewed-container').innerHTML = '';
    }
}

// Get product ID from data attribute and initialize recently viewed functionality
document.addEventListener('DOMContentLoaded', function() {
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
        }
    }
}); 