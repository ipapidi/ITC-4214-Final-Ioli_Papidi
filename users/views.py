from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from .forms import UserRegistrationForm
from .models import UserProfile, Wishlist, RecentlyViewed
from products.models import Product
from products.forms import VendorProductForm
from django.http import JsonResponse
from products.models import Category, Brand


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save()
            
            # Handle vendor registration
            is_vendor = form.cleaned_data.get('is_vendor', False)
            vendor_team = form.cleaned_data.get('vendor_team', '')
            
            if is_vendor and vendor_team:
                # Update user profile with vendor information
                profile = user.profile
                profile.is_vendor = True
                profile.vendor_status = 'pending'
                profile.vendor_team = vendor_team
                profile.vendor_application_date = timezone.now()
                profile.save()
                
                messages.success(request, 'Account created successfully! Your vendor application is pending approval.')
            else:
                messages.success(request, 'Account created successfully!')
            
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # get user data
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
    # Handle profile editing
    if request.method == 'POST':
        # Validate phone number
        phone_number = request.POST.get('phone_number', '')
        if phone_number and not phone_number.isdigit():
            messages.error(request, 'Phone number must contain only digits.')
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
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    # For GET requests, redirect to profile page (edit is handled via modal)
    return redirect('users:profile')


@login_required
def change_password(request):
    # Handle password change
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
    # get wishlist items
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
    # add to wishlist
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
    # remove from wishlist
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed', 'product_id': product_id})
    messages.success(request, f'{product.name} removed from wishlist!')
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('users:wishlist')


# Vendor Dashboard Views
@login_required
def vendor_dashboard(request):
    """
    Vendor dashboard - only accessible to verified vendors
    Shows vendor's own products and management options
    """
    # Check if user is a verified vendor
    if not request.user.profile.is_verified_vendor():
        messages.error(request, 'Access denied. Only verified vendors can access the vendor dashboard.')
        return redirect('users:profile')
    
    # Get vendor's products
    vendor_products = Product.objects.filter(vendor=request.user.profile).order_by('-created_at')
    
    context = {
        'vendor_products': vendor_products,
        'vendor_profile': request.user.profile,
    }
    return render(request, 'users/vendor_dashboard.html', context)


@login_required
def vendor_product_create(request):
    """
    Create new product for vendor
    """
    # Check if user is a verified vendor
    if not request.user.profile.is_verified_vendor():
        messages.error(request, 'Access denied. Only verified vendors can create products.')
        return redirect('users:profile')
    
    if request.method == 'POST':
        form = VendorProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Get the F1 team brand for this vendor
                vendor_team = request.user.profile.vendor_team
                brand, created = Brand.objects.get_or_create(
                    name=vendor_team,
                    defaults={
                        'is_f1_team': True,
                        'description': f'Authentic F1 parts from {vendor_team}',
                        'is_active': True
                    }
                )
                
                # Create the product with form data
                product = form.save(commit=False)
                product.vendor = request.user.profile
                product.brand = brand  # Set the brand automatically
                product.is_authentic_f1_part = True
                
                # Handle subcategory - if not provided, use first subcategory of selected category
                if not product.subcategory:
                    product.subcategory = product.category.subcategories.first()
                
                product.sku = f"VENDOR-{request.user.id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                product.save()
                
                messages.success(request, f'Product "{product.name}" created successfully!')
                return redirect('users:vendor_dashboard')
            except Exception as e:
                messages.error(request, f'Error creating product: {str(e)}')
        else:
            # show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VendorProductForm()
    
    context = {
        'form': form,
    }
    return render(request, 'users/vendor_product_form.html', context)


@login_required
def vendor_product_edit(request, product_id):
    """
    Edit vendor's own product
    """
    # Check if user is a verified vendor
    if not request.user.profile.is_verified_vendor():
        messages.error(request, 'Access denied. Only verified vendors can edit products.')
        return redirect('users:profile')
    
    # Get the product and check ownership
    product = get_object_or_404(Product, id=product_id)
    if product.vendor != request.user.profile:
        messages.error(request, 'Access denied. You can only edit your own products.')
        return redirect('users:vendor_dashboard')
    
    if request.method == 'POST':
        form = VendorProductForm(request.POST, request.FILES, instance=product)
        clear_image = request.POST.get('clear_image')
        if form.is_valid():
            try:
                if clear_image == '1':
                    # Remove the image and delete from storage
                    if product.main_image:
                        product.main_image.delete(save=False)
                    product.main_image = None
                
                # Save the form but ensure brand is set correctly
                product = form.save(commit=False)
                # Ensure brand is set to vendor's team
                vendor_team = request.user.profile.vendor_team
                brand, created = Brand.objects.get_or_create(
                    name=vendor_team,
                    defaults={
                        'is_f1_team': True,
                        'description': f'Authentic F1 parts from {vendor_team}',
                        'is_active': True
                    }
                )
                product.brand = brand
                product.save()
                
                messages.success(request, f'Product "{product.name}" updated successfully!')
                return redirect('users:vendor_dashboard')
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
        else:
            # Form validation failed - show errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = VendorProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'users/vendor_product_form.html', context)


@login_required
def vendor_product_delete(request, product_id):
    """
    Delete vendor's own product
    """
    # Check if user is a verified vendor
    if not request.user.profile.is_verified_vendor():
        messages.error(request, 'Access denied. Only verified vendors can delete products.')
        return redirect('users:profile')
    
    # Get the product and check ownership
    product = get_object_or_404(Product, id=product_id)
    if product.vendor != request.user.profile:
        messages.error(request, 'Access denied. You can only delete your own products.')
        return redirect('users:vendor_dashboard')
    
    if request.method == 'POST':
        # delete product
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('users:vendor_dashboard')
    
    context = {
        'product': product,
    }
    return render(request, 'users/vendor_product_confirm_delete.html', context)
