from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Review, ReviewVote, ProductRating
from products.models import Product


def product_reviews(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.filter(is_approved=True)
    
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'reviews/product_reviews.html', context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        pros = request.POST.get('pros', '')
        cons = request.POST.get('cons', '')
        
        review, created = Review.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                'rating': rating,
                'title': title,
                'content': content,
                'pros': pros,
                'cons': cons,
            }
        )
        
        if not created:
            review.rating = rating
            review.title = title
            review.content = content
            review.pros = pros
            review.cons = cons
            review.save()
        
        messages.success(request, 'Review submitted successfully!')
        return redirect('products:product_detail', slug=product.slug)
    
    return render(request, 'reviews/add_review.html', {'product': product})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        review.rating = int(request.POST.get('rating', 5))
        review.title = request.POST.get('title', '')
        review.content = request.POST.get('content', '')
        review.pros = request.POST.get('pros', '')
        review.cons = request.POST.get('cons', '')
        review.save()
        
        messages.success(request, 'Review updated successfully!')
        return redirect('products:product_detail', slug=review.product.slug)
    
    return render(request, 'reviews/edit_review.html', {'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_slug = review.product.slug
    review.delete()
    
    messages.success(request, 'Review deleted successfully!')
    return redirect('products:product_detail', slug=product_slug)


@login_required
def vote_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        vote_type = request.POST.get('vote_type')
        
        if vote_type in ['helpful', 'unhelpful']:
            vote, created = ReviewVote.objects.get_or_create(
                review=review,
                user=request.user,
                defaults={'vote_type': vote_type}
            )
            
            if not created:
                vote.vote_type = vote_type
                vote.save()
            
            return JsonResponse({
                'success': True,
                'helpful_count': review.helpful_votes.count(),
                'unhelpful_count': review.unhelpful_votes.count()
            })
    
    return JsonResponse({'success': False})


@login_required
def report_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        reason = request.POST.get('reason', '')
        description = request.POST.get('description', '')
        
        from .models import ReviewReport
        report, created = ReviewReport.objects.get_or_create(
            review=review,
            reporter=request.user,
            defaults={
                'reason': reason,
                'description': description
            }
        )
        
        if created:
            messages.success(request, 'Review reported successfully!')
        else:
            messages.info(request, 'You have already reported this review!')
        
        return redirect('products:product_detail', slug=review.product.slug)
    
    return render(request, 'reviews/report_review.html', {'review': review})
