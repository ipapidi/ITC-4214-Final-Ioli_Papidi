from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Review, ProductRating
from products.models import Product


def product_reviews(request, product_id): #Display all reviews for a product
    """Display all reviews for a product"""
    product = get_object_or_404(Product, id=product_id) #Get the product
    reviews = product.reviews.all() #Get the reviews
    
    context = {
        'product': product, #Set the product
        'reviews': reviews, #Set the reviews
    }
    return render(request, 'reviews/product_reviews.html', context)


@login_required #Login required
def add_review(request, product_id): #Add a rating for a product
    """Add a rating for a product"""
    product = get_object_or_404(Product, id=product_id) #Get the product
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5)) #Get the rating
        
        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Rating must be between 1 and 5.') #Set the error message
            return redirect('products:product_detail', slug=product.slug) #Redirect to the product detail page
        
        # Create or update rating
        review, created = Review.objects.get_or_create( #Get or create the review
            user=request.user, #Set the user
            product=product, #Set the product
            defaults={'rating': rating} #Set the rating
        )
        
        if not created:
            # Update existing rating
            review.rating = rating
            review.save() #Save the review
        
        messages.success(request, 'Rating submitted successfully!') #Set the success message
        return redirect('products:product_detail', slug=product.slug) #Redirect to the product detail page
    
    return render(request, 'reviews/add_review.html', {'product': product}) #Render the add review page


@login_required #Login required
def edit_review(request, review_id): #Edit a rating
    """Edit a rating"""
    review = get_object_or_404(Review, id=review_id, user=request.user) #Get the review
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5)) #Get the rating
        
        # Validate rating
        if rating < 1 or rating > 5:
            messages.error(request, 'Rating must be between 1 and 5.') #Set the error message
            return redirect('products:product_detail', slug=review.product.slug) #Redirect to the product detail page
        
        review.rating = rating #Set the rating
        review.save() #Save the review
        
        messages.success(request, 'Rating updated successfully!') #Set the success message
        return redirect('products:product_detail', slug=review.product.slug) #Redirect to the product detail page
    
    return render(request, 'reviews/edit_review.html', {'review': review}) #Render the edit review page


@login_required #Login required
def delete_review(request, review_id): #Delete a rating
    """Delete a rating"""
    review = get_object_or_404(Review, id=review_id, user=request.user) #Get the review
    product_slug = review.product.slug #Get the product slug
    review.delete() #Delete the review
    
    messages.success(request, 'Rating deleted successfully!') #Set the success message
    return redirect('products:product_detail', slug=product_slug) #Redirect to the product detail page
