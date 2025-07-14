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