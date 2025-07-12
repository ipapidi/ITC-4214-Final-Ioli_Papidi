from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Case, When, F, DecimalField
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, SubCategory, Brand, ProductRating
from .forms import ProductRatingForm
from users.models import Wishlist
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


def home(request):
    # get featured products
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:6]
    categories = Category.objects.filter(is_active=True)[:9]
    
    # Add wishlist status for featured products
    for product in featured_products:
        if request.user.is_authenticated:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        else:
            product.is_in_wishlist = False

    # Dynamically set icon_url for each category
    for category in categories:
        if category.image:
            category.icon_url = category.image.url
        else:
            # Assume icon filename matches the category name (capitalized, no spaces, .png)
            icon_filename = f"{category.name.replace(' ', '')}.png"
            category.icon_url = f"/media/categories/{icon_filename}"

    context = {
        'featured_products': featured_products,
        'bestsellers': bestsellers,
        'categories': categories,
    }
    return render(request, 'products/home.html', context)


def product_list(request):
    # get all products
    products = Product.objects.filter(is_active=True)

    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    brand = request.GET.get('brand')
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')

    # filter by category
    if category:
        products = products.filter(category__slug=category)
    if subcategory:
        products = products.filter(subcategory__slug=subcategory)
    if brand:
        products = products.filter(brand__slug=brand)

    # sort products
    if sort_by == 'price':
        # Sort by current price (sale_price if available, otherwise price)
        products = products.annotate(
            sort_price=Case(
                When(sale_price__isnull=False, then=F('sale_price')),
                default=F('price'),
                output_field=DecimalField(),
            )
        )
        order = 'sort_price' if sort_order == 'asc' else '-sort_price'
    elif sort_by == 'Rating':
        # Sort by average rating
        products = products.annotate(avg_rating=Avg('ratings__rating'))
        order = 'avg_rating' if sort_order == 'asc' else '-avg_rating'
    elif sort_by == 'newest':
        order = 'created_at' if sort_order == 'asc' else '-created_at'
    else:
        # Default to name sorting
        order = 'name' if sort_order == 'asc' else '-name'
    products = products.order_by(order)

    # get subcategories
    subcategories = []
    if category:
        try:
            selected_category = Category.objects.get(slug=category)
            subcategories = selected_category.subcategories.filter(is_active=True)
        except Category.DoesNotExist:
            subcategories = []

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Add star_rating property for each product (0-5 stars)
    for product in page_obj:
        # Add wishlist status for authenticated users
        if request.user.is_authenticated:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        else:
            product.is_in_wishlist = False

    # Get categories and brands for filters
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)

    # Create current_filters dict for template
    current_filters = {
        'category': category,
        'subcategory': subcategory,
        'brand': brand,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }

    context = {
        'products': page_obj,
        'categories': categories,
        'brands': brands,
        'subcategories': subcategories,
        'selected_category': category,
        'selected_subcategory': subcategory,
        'selected_brand': brand,
        'sort_by': sort_by,
        'sort_order': sort_order,
        'current_filters': current_filters,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    # get product by slug
    product = get_object_or_404(Product, slug=slug, is_active=True)
    user_rating = None
    is_in_wishlist = False
    
    if request.user.is_authenticated:
        # get user rating
        user_rating = ProductRating.objects.filter(product=product, user=request.user).first()
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()
        if request.method == 'POST':
            # handle rating form
            form = ProductRatingForm(request.POST, instance=user_rating)
            if form.is_valid():
                rating_obj = form.save(commit=False)
                rating_obj.product = product
                rating_obj.user = request.user
                rating_obj.save()
                messages.success(request, 'Your rating has been submitted!')
                return redirect('products:product_detail', slug=slug)
        else:
            form = ProductRatingForm(instance=user_rating)
    else:
        form = None
    
    # Content-based recommender: prioritize same category and brand, then category, then any
    recommended_qs = Product.objects.filter(
        is_active=True
    ).exclude(id=product.id)
    same_cat_brand = recommended_qs.filter(category=product.category, brand=product.brand)
    recommended_products = list(same_cat_brand.annotate(annotated_avg_rating=Avg('ratings__rating')).order_by('-annotated_avg_rating')[:3])
    if len(recommended_products) < 3:
        needed = 3 - len(recommended_products)
        same_cat = recommended_qs.filter(category=product.category).exclude(id__in=[p.id for p in recommended_products])
        recommended_products += list(same_cat.annotate(annotated_avg_rating=Avg('ratings__rating')).order_by('-annotated_avg_rating')[:needed])
    if len(recommended_products) < 3:
        needed = 3 - len(recommended_products)
        any_products = recommended_qs.exclude(id__in=[p.id for p in recommended_products])
        recommended_products += list(any_products.annotate(annotated_avg_rating=Avg('ratings__rating')).order_by('-annotated_avg_rating')[:needed])
    context = {
        'product': product,
        'related_products': Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)[:4],
        'form': form,
        'user_rating': user_rating,
        'is_in_wishlist': is_in_wishlist,
        'recommended_products': recommended_products,
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug):
    # get category by slug
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
    }
    return render(request, 'products/category_detail.html', context)


def subcategory_detail(request, category_slug, subcategory_slug):
    # get subcategory by slug
    subcategory = get_object_or_404(
        SubCategory, 
        slug=subcategory_slug,
        category__slug=category_slug,
        is_active=True
    )
    products = Product.objects.filter(subcategory=subcategory, is_active=True)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'subcategory': subcategory,
        'products': page_obj,
    }
    return render(request, 'products/subcategory_detail.html', context)


def brand_detail(request, slug):
    # get brand by slug
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    products = Product.objects.filter(brand=brand, is_active=True)
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'brand': brand,
        'products': page_obj,
    }
    return render(request, 'products/brand_detail.html', context)


def search(request):
    # get search query
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)

    # Keywords that should redirect to contact page
    contact_keywords = [
        'contact', 'phone', 'email', 'support', 'help', 'map', 'location', 'address', 'customer service', 'call', 'find us', 'where', 'reach us', 'get in touch'
    ]
    if query.lower() in contact_keywords:
        return redirect('products:contact')

    if query:
        # filter by search
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(keywords__icontains=query)
        ).distinct()

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # For advanced search bar (dropdowns, etc.)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    subcategories = SubCategory.objects.filter(is_active=True)

    context = {
        'products': page_obj,
        'query': query,
        'categories': categories,
        'brands': brands,
        'subcategories': subcategories,
    }
    return render(request, 'products/search_results.html', context)


def about(request):
    # about page
    return render(request, 'products/about.html')


def contact(request):
    # Contact page
    return render(request, 'products/contact.html')


@csrf_exempt
def recently_viewed(request):
    if request.method == "POST":
        # get recently viewed ids
        data = json.loads(request.body)
        ids = data.get('viewed', [])[:3]
        products_qs = Product.objects.filter(id__in=ids)
        products_dict = {str(p.id): p for p in products_qs}
        products = [products_dict[str(i)] for i in ids if str(i) in products_dict]
        products_html = render_to_string('products/_recently_viewed.html', {'products': products})
        return JsonResponse({'products_html': products_html})
    return JsonResponse({'products_html': ''})


@csrf_exempt
def get_subcategories(request):
    # AJAX endpoint to get subcategories for a given category
    category_slug = request.GET.get('category')
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug, is_active=True)
            subcategories = category.subcategories.filter(is_active=True)
            data = {
                'subcategories': [
                    {'slug': subcat.slug, 'name': subcat.name}
                    for subcat in subcategories
                ]
            }
        except Category.DoesNotExist:
            data = {'subcategories': []}
    else:
        data = {'subcategories': []}
    
    return JsonResponse(data)
