from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm
from .models import UserProfile, Wishlist, RecentlyViewed
from products.models import Product
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    recent_orders = user.orders.all()[:5]
    wishlist_items = user.wishlist_items.all()[:6]
    recently_viewed = user.recently_viewed.all()[:6]
    
    context = {
        'user': user,
        'recent_orders': recent_orders,
        'wishlist_items': wishlist_items,
        'recently_viewed': recently_viewed,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """
    Handle profile editing for authenticated users.
    Updates both User model fields and UserProfile model fields.
    Username cannot be changed for security reasons.
    """
    if request.method == 'POST':
        # Validate phone number and car year
        phone_number = request.POST.get('phone_number', '')
        primary_car_year = request.POST.get('primary_car_year', '')
        if phone_number and not phone_number.isdigit():
            messages.error(request, 'Phone number must contain only digits.')
            return redirect('users:profile')
        if primary_car_year and not primary_car_year.isdigit():
            messages.error(request, 'Car year must be a valid number.')
            return redirect('users:profile')
        # Update User model fields (first_name, last_name, email)
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        # Update UserProfile model fields
        profile = request.user.profile
        profile.phone_number = phone_number
        profile.primary_car_make = request.POST.get('primary_car_make', '')
        profile.primary_car_model = request.POST.get('primary_car_model', '')
        profile.primary_car_year = int(primary_car_year) if primary_car_year else None
        profile.favorite_f1_team = request.POST.get('favorite_f1_team', '')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    # For GET requests, redirect to profile page (edit is handled via modal)
    return redirect('users:profile')


@login_required
def change_password(request):
    """
    Handle password change for authenticated users.
    Uses Django's built-in PasswordChangeForm for security.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update session to prevent logout after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('users:profile')
        else:
            # If form is invalid, show error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return redirect('users:profile')
    
    # For GET requests, redirect to profile page (password change is handled via modal)
    return redirect('users:profile')


@login_required
def wishlist(request):
    wishlist_items = request.user.wishlist_items.all()
    # Mark all products as in wishlist for the template
    for item in wishlist_items:
        item.product.is_in_wishlist = True
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'users/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added', 'product_id': product_id})
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('products:product_detail', slug=product.slug)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed', 'product_id': product_id})
    messages.success(request, f'{product.name} removed from wishlist!')
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('users:wishlist')
