from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, SubCategory, Brand, Product, ProductImage, ProductSpecification


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for product categories.
    F1-inspired category management.
    """
    list_display = ['name', 'slug', 'product_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon_class')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def product_count(self, obj):
        """Display number of products in category"""
        count = obj.products.count()
        return format_html('<span style="color: #e74c3c; font-weight: bold;">{}</span>', count)
    product_count.short_description = 'Products'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for product subcategories.
    """
    list_display = ['name', 'category', 'product_count', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']

    def product_count(self, obj):
        """Display number of products in subcategory"""
        count = obj.products.count()
        return format_html('<span style="color: #e74c3c; font-weight: bold;">{}</span>', count)
    product_count.short_description = 'Products'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin interface for car part brands.
    Includes F1 team branding options.
    """
    list_display = ['name', 'logo_display', 'is_f1_team', 'product_count', 'is_active', 'created_at']
    list_filter = ['is_f1_team', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'website')
        }),
        ('Branding', {
            'fields': ('logo', 'is_f1_team')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def logo_display(self, obj):
        """Display brand logo in admin list"""
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 50px;" />', obj.logo.url)
        return "No Logo"
    logo_display.short_description = 'Logo'

    def product_count(self, obj):
        """Display number of products by brand"""
        count = obj.products.count()
        return format_html('<span style="color: #e74c3c; font-weight: bold;">{}</span>', count)
    product_count.short_description = 'Products'


class ProductImageInline(admin.TabularInline):
    """
    Inline admin for product images.
    """
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']


class ProductSpecificationInline(admin.TabularInline):
    """
    Inline admin for product specifications.
    """
    model = ProductSpecification
    extra = 1
    fields = ['name', 'value', 'unit', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for products.
    Comprehensive F1-inspired product management.
    """
    list_display = [
        'name', 'brand', 'category', 'price_display', 'stock_status_display', 
        'performance_rating', 'is_featured', 'is_active', 'created_at'
    ]
    list_filter = [
        'category', 'subcategory', 'brand', 'is_active', 'is_featured', 
        'is_bestseller', 'installation_difficulty', 'created_at'
    ]
    search_fields = ['name', 'sku', 'description', 'brand__name', 'category__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'discount_percentage_display']
    
    inlines = [ProductImageInline, ProductSpecificationInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'description', 'features')
        }),
        ('Categorization', {
            'fields': ('category', 'subcategory', 'brand')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price', 'cost_price', 'discount_percentage_display')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'min_stock_level')
        }),
        ('Performance Metrics', {
            'fields': ('performance_rating', 'weight_savings', 'power_gain'),
            'description': 'F1-inspired performance metrics'
        }),
        ('Compatibility', {
            'fields': ('compatible_cars', 'installation_difficulty')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Status & Visibility', {
            'fields': ('is_active', 'is_featured', 'is_bestseller')
        }),
        ('SEO & Marketing', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',)
        }),
        ('Technical Specifications', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        """Display price with sale indicator"""
        if obj.is_on_sale:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">${}</span><br>'
                '<span style="color: #e74c3c; font-weight: bold;">${}</span>',
                obj.price, obj.sale_price
            )
        return format_html('<span style="font-weight: bold;">${}</span>', obj.price)
    price_display.short_description = 'Price'

    def stock_status_display(self, obj):
        """Display stock status with color coding"""
        status = obj.stock_status
        if status == 'out_of_stock':
            return format_html('<span style="color: #e74c3c; font-weight: bold;">Out of Stock</span>')
        elif status == 'low_stock':
            return format_html('<span style="color: #f39c12; font-weight: bold;">Low Stock ({})</span>', obj.stock_quantity)
        else:
            return format_html('<span style="color: #27ae60; font-weight: bold;">In Stock ({})</span>', obj.stock_quantity)
    stock_status_display.short_description = 'Stock'

    def discount_percentage_display(self, obj):
        """Display discount percentage"""
        if obj.is_on_sale:
            return format_html('<span style="color: #e74c3c; font-weight: bold;">{}% OFF</span>', obj.discount_percentage)
        return "No discount"
    discount_percentage_display.short_description = 'Discount'

    def get_queryset(self, request):
        """Optimize queryset with related fields"""
        return super().get_queryset(request).select_related('brand', 'category', 'subcategory')

    actions = ['mark_featured', 'mark_bestseller', 'activate_products', 'deactivate_products']

    def mark_featured(self, request, queryset):
        """Mark selected products as featured"""
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} products marked as featured.')
    mark_featured.short_description = "Mark selected products as featured"

    def mark_bestseller(self, request, queryset):
        """Mark selected products as bestsellers"""
        updated = queryset.update(is_bestseller=True)
        self.message_user(request, f'{updated} products marked as bestsellers.')
    mark_bestseller.short_description = "Mark selected products as bestsellers"

    def activate_products(self, request, queryset):
        """Activate selected products"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} products activated.')
    activate_products.short_description = "Activate selected products"

    def deactivate_products(self, request, queryset):
        """Deactivate selected products"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} products deactivated.')
    deactivate_products.short_description = "Deactivate selected products"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin interface for product images.
    """
    list_display = ['product', 'image_display', 'is_primary', 'order', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['created_at']

    def image_display(self, obj):
        """Display product image in admin list"""
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "No Image"
    image_display.short_description = 'Image'


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    """
    Admin interface for product specifications.
    """
    list_display = ['product', 'name', 'value', 'unit', 'order']
    list_filter = ['order']
    search_fields = ['product__name', 'name', 'value']
    ordering = ['product', 'order']
