from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserProfile, Wishlist, RecentlyViewed
from products.models import Product


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
    if request.method == 'POST':
        profile = request.user.profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.primary_car_make = request.POST.get('primary_car_make', '')
        profile.primary_car_model = request.POST.get('primary_car_model', '')
        profile.primary_car_year = request.POST.get('primary_car_year', '')
        profile.favorite_f1_team = request.POST.get('favorite_f1_team', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    return render(request, 'users/edit_profile.html')


@login_required
def wishlist(request):
    wishlist_items = request.user.wishlist_items.all()
    
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
    
    if created:
        messages.success(request, f'{product.name} added to wishlist!')
    else:
        messages.info(request, f'{product.name} is already in your wishlist!')
    
    return redirect('products:product_detail', slug=product.slug)


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f'{product.name} removed from wishlist!')
    
    return redirect('users:wishlist')
