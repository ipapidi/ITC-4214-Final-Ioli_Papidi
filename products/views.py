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
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6] #Gets the featured products
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:6] #Gets the bestsellers
    categories = Category.objects.filter(is_active=True)[:9] #Gets the categories
    
    # Add wishlist status for featured products
    for product in featured_products:
        if request.user.is_authenticated:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists() #Checks if the product is in the wishlist
        else:
            product.is_in_wishlist = False #Sets the is_in_wishlist to False

    # Dynamically set icon_url for each category
    for category in categories:
        if category.image:
            category.icon_url = category.image.url #Sets the icon_url to the image url
        else:
            # Assume icon filename matches the category name (capitalized, no spaces, .png)
            icon_filename = f"{category.name.replace(' ', '')}.png" #Sets the icon_filename to the category name
            category.icon_url = f"/media/categories/{icon_filename}" #Sets the icon_url to the icon_filename

    context = {
        'featured_products': featured_products, #Sets the featured products to the context
        'bestsellers': bestsellers, #Sets the bestsellers products to the context
        'categories': categories, #Sets the categories to the context
    }
    return render(request, 'products/home.html', context) #Renders the home page


def product_list(request):
    # get all products
    products = Product.objects.filter(is_active=True) #Gets the products

    category = request.GET.get('category') #Gets the category
    subcategory = request.GET.get('subcategory') #Gets the subcategory
    brand = request.GET.get('brand') #Gets the brand
    sort_by = request.GET.get('sort_by', 'name') #Gets the sort by
    sort_order = request.GET.get('sort_order', 'asc') #Gets the sort order

    # filter by category
    if category:
        products = products.filter(category__slug=category) #Filters the products by category
    if subcategory:
        products = products.filter(subcategory__slug=subcategory) #Filters the products by subcategory
    if brand:
        products = products.filter(brand__slug=brand) #Filters the products by brand

    # sort products
    if sort_by == 'price':
        # Sort by current price (sale_price if available, otherwise price)
        products = products.annotate(
            sort_price=Case(
                When(sale_price__isnull=False, then=F('sale_price')), #When the sale price is not null, then set the sort price to the sale price
                default=F('price'), #Default to the price
                output_field=DecimalField(), #Set the output field to DecimalField
            )
        )
        order = 'sort_price' if sort_order == 'asc' else '-sort_price' #Sets the order to the sort price
    elif sort_by == 'Rating':
        # Sort by average rating
        products = products.annotate(avg_rating=Avg('ratings__rating')) #Annotates the products by average rating
        order = 'avg_rating' if sort_order == 'asc' else '-avg_rating' #Sets the order to the average rating
    elif sort_by == 'newest':
        order = 'created_at' if sort_order == 'asc' else '-created_at' #Sets the order to the created at
    else:
        # Default to name sorting
        order = 'name' if sort_order == 'asc' else '-name' #Sets the order to the name
    products = products.order_by(order) #Orders the products by the order

    # get subcategories
    subcategories = []
    if category:
        try:
            selected_category = Category.objects.get(slug=category) #Gets the selected category
            subcategories = selected_category.subcategories.filter(is_active=True) #Filters the subcategories by active
        except Category.DoesNotExist:
            subcategories = [] #Sets the subcategories to an empty list

    paginator = Paginator(products, 12) #Creates a paginator with 12 products per page
    page_number = request.GET.get('page') #Gets the page number
    page_obj = paginator.get_page(page_number) #Gets the page object

    # Add star_rating property for each product (0-5 stars)
    for product in page_obj:
        # Add wishlist status for authenticated users
        if request.user.is_authenticated:
            product.is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists() #Checks if the product is in the wishlist
        else:
            product.is_in_wishlist = False #Sets the is_in_wishlist to False

    # Get categories and brands for filters
    categories = Category.objects.filter(is_active=True) #Gets the categories
    brands = Brand.objects.filter(is_active=True) #Gets the brands

    # Create current_filters dict for template
    current_filters = {
        'category': category, #Sets the category to the current filters
        'subcategory': subcategory, #Sets the subcategory to the current filters
        'brand': brand, #Sets the brand to the current filters
        'sort_by': sort_by, #Sets the sort by to the current filters
        'sort_order': sort_order, #Sets the sort order to the current filters
    }

    context = {
        'products': page_obj, #Sets the products to the context
        'categories': categories, #Sets the categories to the context
        'brands': brands, #Sets the brands to the context
        'subcategories': subcategories, #Sets the subcategories to the context
        'selected_category': category, #Sets the selected category to the context
        'selected_subcategory': subcategory, #Sets the selected subcategory to the context
        'selected_brand': brand, #Sets the selected brand to the context
        'sort_by': sort_by, #Sets the sort by to the context
        'sort_order': sort_order, #Sets the sort order to the context
        'current_filters': current_filters, #Sets the current filters to the context
    }
    return render(request, 'products/product_list.html', context) #Renders the product list page


def product_detail(request, slug):
    # get product by slug
    product = get_object_or_404(Product, slug=slug, is_active=True)
    user_rating = None
    is_in_wishlist = False
    
    if request.user.is_authenticated:
        # get user rating
        user_rating = ProductRating.objects.filter(product=product, user=request.user).first() #Gets the user rating
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists() #Checks if the product is in the wishlist
        if request.method == 'POST':
            # handle rating form
            form = ProductRatingForm(request.POST, instance=user_rating) #Creates a form for the user rating
            if form.is_valid():
                rating_obj = form.save(commit=False) #Saves the rating object
                rating_obj.product = product #Sets the product to the rating object
                rating_obj.user = request.user #Sets the user to the rating object
                rating_obj.save() #Saves the rating object
                messages.success(request, 'Your rating has been submitted!') #Displays a success message
                return redirect('products:product_detail', slug=slug) #Redirects to the product detail page
        else:
            form = ProductRatingForm(instance=user_rating) #Creates a form for the user rating
    else:
        form = None #Sets the form to None
    
    # Content-based recommender: prioritize same category and brand, then category, then any
    recommended_qs = Product.objects.filter(
        is_active=True
    ).exclude(id=product.id)
    same_cat_brand = recommended_qs.filter(category=product.category, brand=product.brand) #Filters the recommended products by category and brand
    recommended_products = list(same_cat_brand.annotate(annotated_avg_rating=Avg('ratings__rating')).order_by('-annotated_avg_rating')[:3]) #Annotates the recommended products by average rating and orders them by the average rating
    if len(recommended_products) < 3: #Checks if the recommended products are less than 3
        needed = 3 - len(recommended_products) #Sets the needed to the difference between 3 and the length of the recommended products
        same_cat = recommended_qs.filter(category=product.category).exclude(id__in=[p.id for p in recommended_products]) #Filters the recommended products by category and excludes the products in the recommended products
        recommended_products += list(same_cat.annotate(annotated_avg_rating=Avg('ratings__rating')).order_by('-annotated_avg_rating')[:needed]) #Annotates the recommended products by average rating and orders them by the average rating
    if len(recommended_products) < 3: #Checks if the recommended products are less than 3
        needed = 3 - len(recommended_products) #Sets the needed to the difference between 3 and the length of the recommended products
        any_products = recommended_qs.exclude(id__in=[p.id for p in recommended_products]) #Filters the recommended products by excluding the products in the recommended products
        recommended_products += list(any_products.annotate(annotated_avg_rating=Avg('ratings__rating')).order_by('-annotated_avg_rating')[:needed]) #Annotates the recommended products by average rating and orders them by the average rating
    context = {
        'product': product, #Sets the product to the context
        'related_products': Product.objects.filter(
            category=product.category, #Filters the related products by category
            is_active=True #Filters the related products by active
        ).exclude(id=product.id)[:4], #Filters the related products by excluding the product
        'form': form,
        'user_rating': user_rating, #Sets the user rating to the context
        'is_in_wishlist': is_in_wishlist, #Sets the is in wishlist to the context
        'recommended_products': recommended_products, #Sets the recommended
    }
    return render(request, 'products/product_detail.html', context)


def category_detail(request, slug): #Category detail view
    # get category by slug
    category = get_object_or_404(Category, slug=slug, is_active=True) #Gets the category by slug
    products = Product.objects.filter(category=category, is_active=True) #Gets the products by category and active
    
    paginator = Paginator(products, 12) #Creates a paginator with 12 products per page
    page_number = request.GET.get('page') #Gets the page number
    page_obj = paginator.get_page(page_number) #Gets the page object
    
    context = {
        'category': category, #Sets the category to the context
        'products': page_obj, #Sets the products to the context
    }
    return render(request, 'products/category_detail.html', context)


def subcategory_detail(request, category_slug, subcategory_slug): #Subcategory detail view
    # get subcategory by slug
    subcategory = get_object_or_404(
        SubCategory, 
        slug=subcategory_slug,
        category__slug=category_slug,
        is_active=True
    )
    products = Product.objects.filter(subcategory=subcategory, is_active=True) #Gets the products by subcategory and active
    
    paginator = Paginator(products, 12) #Creates a paginator with 12 products per page
    page_number = request.GET.get('page') #Gets the page number
    page_obj = paginator.get_page(page_number) #Gets the page object
    
    context = {
        'subcategory': subcategory, #Sets the subcategory to the context
        'products': page_obj, #Sets the products to the context
    }
    return render(request, 'products/subcategory_detail.html', context)


def brand_detail(request, slug):
    # get brand by slug
    brand = get_object_or_404(Brand, slug=slug, is_active=True) #Gets the brand by slug
    products = Product.objects.filter(brand=brand, is_active=True) #Gets the products by brand and active
    
    paginator = Paginator(products, 12) #Creates a paginator with 12 products per page
    page_number = request.GET.get('page') #Gets the page number
    page_obj = paginator.get_page(page_number) #Gets the page object
    
    context = {
        'brand': brand, #Sets the brand to the context
        'products': page_obj, #Sets the products to the context
    }
    return render(request, 'products/brand_detail.html', context)


def search(request): #Search view
    # get search query
    query = request.GET.get('q', '').strip() #Gets the search query
    products = Product.objects.filter(is_active=True) #Gets the products by active

    # Keywords that should redirect to contact page
    contact_keywords = [
        'contact', 'phone', 'email', 'support', 'help', 'map', 'location', 'address', 'customer service', 'call', 'find us', 'where', 'reach us', 'get in touch'
    ]
    if query.lower() in contact_keywords: #Checks if the search query is in the contact keywords
        return redirect('products:contact') #Redirects to the contact page

    if query:
        # filter by search
        products = products.filter(
            Q(name__icontains=query) | #Filters the products by name
            Q(description__icontains=query) | #Filters the products by description
            Q(brand__name__icontains=query) | #Filters the products by brand
            Q(category__name__icontains=query) | #Filters the products by category
            Q(subcategory__name__icontains=query) |
            Q(keywords__icontains=query)
        ).distinct()

    paginator = Paginator(products, 12) #Creates a paginator with 12 products per page
    page_number = request.GET.get('page') #Gets the page number
    page_obj = paginator.get_page(page_number) #Gets the page object

    # For advanced search bar (dropdowns, etc.)
    categories = Category.objects.filter(is_active=True) #Gets the categories by active
    brands = Brand.objects.filter(is_active=True) #Gets the brands by active
    subcategories = SubCategory.objects.filter(is_active=True) #Gets the subcategories by active

    context = {
        'products': page_obj, #Sets the products to the context
        'query': query, #Sets the query to the context
        'categories': categories, #Sets the categories to the context
        'brands': brands, #Sets the brands to the context
        'subcategories': subcategories, #Sets the subcategories to the context
    }
    return render(request, 'products/search_results.html', context)


def about(request): #About view
    # about page
    return render(request, 'products/about.html')


def contact(request): #Contact view
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '').strip() 
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not name:
            messages.error(request, 'Please enter your name.')
        elif not email:
            messages.error(request, 'Please enter your email address.')
        elif '@' not in email:
            messages.error(request, 'Please enter a valid email address.')
        elif not message:
            messages.error(request, 'Please enter your message.')
        elif len(message) < 10:
            messages.error(request, 'Your message must be at least 10 characters long.')
        else:
            from users.models import ContactMessage
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('products:contact')
    
    return render(request, 'products/contact.html')


@csrf_exempt
def recently_viewed(request): #Recently viewed view
    if request.method == "POST":
        # get recently viewed ids
        data = json.loads(request.body) #Loads the data
        ids = data.get('viewed', [])[:3] #Gets the viewed ids
        products_qs = Product.objects.filter(id__in=ids) #Gets the products by ids
        products_dict = {str(p.id): p for p in products_qs} #Gets the products by ids
        products = [products_dict[str(i)] for i in ids if str(i) in products_dict] #Gets the products by ids
        products_html = render_to_string('products/_recently_viewed.html', {'products': products}) #Renders the recently viewed products
        return JsonResponse({'products_html': products_html}) #Returns the products html
    return JsonResponse({'products_html': ''}) #Returns the products html


@csrf_exempt
def get_subcategories(request): #Get subcategories view
    # AJAX endpoint to get subcategories for a given category
    category_slug = request.GET.get('category') #Gets the category slug
    if category_slug:
        try:
            category = Category.objects.get(slug=category_slug, is_active=True) #Gets the category by slug
            subcategories = category.subcategories.filter(is_active=True) #Gets the subcategories by active
            data = {
                'subcategories': [
                    {'slug': subcat.slug, 'name': subcat.name} #Sets the subcategories to the data
                    for subcat in subcategories
                ]
            }
        except Category.DoesNotExist:
            data = {'subcategories': []} #Sets the subcategories to an empty list
    else:
        data = {'subcategories': []} #Sets the subcategories to an empty list
    
    return JsonResponse(data) #Returns the data
