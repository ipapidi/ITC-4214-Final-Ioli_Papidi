from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Review, ProductRating
from products.models import Product


def product_reviews(request, product_id):
    """Display all reviews for a product"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'reviews/product_reviews.html', context)


@login_required
def add_review(request, product_id):
    """Add a rating for a product"""
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        
        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
            return redirect('products:product_detail', slug=product.slug)
        
        # Create or update rating
        review, created = Review.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'rating': rating}
        )
        
        if not created:
            # Update existing rating
            review.rating = rating
            review.save()
        
        messages.success(request, 'Rating submitted successfully!')
        return redirect('products:product_detail', slug=product.slug)
    
    return render(request, 'reviews/add_review.html', {'product': product})


@login_required
def edit_review(request, review_id):
    """Edit a rating"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        
        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Rating must be between 1 and 5.')
            return redirect('products:product_detail', slug=review.product.slug)
        
        review.rating = rating
        review.save()
        
        messages.success(request, 'Rating updated successfully!')
        return redirect('products:product_detail', slug=review.product.slug)
    
    return render(request, 'reviews/edit_review.html', {'review': review})


@login_required
def delete_review(request, review_id):
    """Delete a rating"""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    
    messages.success(request, 'Rating deleted successfully!')
    return redirect('products:product_detail', slug=product_slug)
