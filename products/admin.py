from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, SubCategory, Brand, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Admin for categories
    list_display = ['name', 'slug', 'product_count', 'is_active', 'created_at'] #Display the fields in the admin interface
    list_filter = ['is_active', 'created_at'] #Filter the fields in the admin interface
    search_fields = ['name', 'description'] #Search the fields in the admin interface
    prepopulated_fields = {'slug': ('name',)} #Pre-populate the slug field with the name field
    readonly_fields = ['created_at', 'updated_at'] #Exclude the fields from the admin interface
    
    fieldsets = ( #Organize the fields in the admin interface
        ('Basic Information', { #Organize the fields in the admin interface
            'fields': ('name', 'slug', 'description', 'icon_class') #Include the fields in the admin interface
        }),
        ('Media', { #Organize the fields in the admin interface
            'fields': ('image',) #Include the fields in the admin interface
        }),
        ('Status', { #Organize the fields in the admin interface
            'fields': ('is_active',) #Include the fields in the admin interface
        }),
        ('Timestamps', { #Organize the fields in the admin interface
            'fields': ('created_at', 'updated_at'), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
    )

    def product_count(self, obj):
        # Display number of products in category
        count = obj.products.count() #Count the number of products in the category
        return format_html('<span style="color: #e74c3c; font-weight: bold;">{}</span>', count) #Display the number of products in the category
    product_count.short_description = 'Products' #Set the short description for the product count field


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    # Admin for subcategories
    list_display = ['name', 'category', 'product_count', 'is_active', 'created_at'] #Display the fields in the admin interface
    list_filter = ['category', 'is_active', 'created_at'] #Filter the fields in the admin interface
    search_fields = ['name', 'description', 'category__name'] #Search the fields in the admin interface
    prepopulated_fields = {'slug': ('name',)} #Pre-populate the slug field with the name field
    readonly_fields = ['created_at'] #Exclude the fields from the admin interface

    def product_count(self, obj):
        # Display number of products in subcategory
        count = obj.products.count() #Count the number of products in the subcategory
        return format_html('<span style="color: #e74c3c; font-weight: bold;">{}</span>', count) #Display the number of products in the subcategory
    product_count.short_description = 'Products' #Set the short description for the product count field


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    # Admin for brands
    list_display = ['name', 'logo_display', 'is_f1_team', 'product_count', 'is_active', 'created_at'] #Display the fields in the admin interface
    list_filter = ['is_f1_team', 'is_active', 'created_at'] #Filter the fields in the admin interface
    search_fields = ['name', 'description'] #Search the fields in the admin interface
    prepopulated_fields = {'slug': ('name',)} #Pre-populate the slug field with the name field
    readonly_fields = ['created_at'] #Exclude the fields from the admin interface
    
    fieldsets = ( #Organize the fields in the admin interface
        ('Basic Information', { #Organize the fields in the admin interface
            'fields': ('name', 'slug', 'description', 'website') #Include the fields in the admin interface
        }),
        ('Branding', { #Organize the fields in the admin interface
            'fields': ('logo', 'is_f1_team') #Include the fields in the admin interface
        }),
        ('Status', { #Organize the fields in the admin interface
            'fields': ('is_active',) #Include the fields in the admin interface
        }),
        ('Timestamps', { #Organize the fields in the admin interface
            'fields': ('created_at',), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
    )

    def logo_display(self, obj):
        # Display brand logo in admin list
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 30px; max-width: 50px;" />', obj.logo.url) #Display the logo in the admin interface
        return "No Logo" #Display the logo in the admin interface
    logo_display.short_description = 'Logo' #Set the short description for the logo field

    def product_count(self, obj):
        # Display number of products by brand
        count = obj.products.count() #Count the number of products in the brand
        return format_html('<span style="color: #e74c3c; font-weight: bold;">{}</span>', count) #Display the number of products in the brand
    product_count.short_description = 'Products' #Set the short description for the product count field


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Admin for products
    list_display = [
        'name', 'brand', 'category', 'price_display', 'stock_status_display', 
        'is_featured', 'is_active', 'created_at'
    ] #Display the fields in the admin interface
    list_filter = [
        'category', 'subcategory', 'brand', 'is_active', 'is_featured', 
        'is_bestseller', 'created_at'
    ] #Filter the fields in the admin interface
    search_fields = ['name', 'sku', 'description', 'brand__name', 'category__name'] #Search the fields in the admin interface
    prepopulated_fields = {'slug': ('name',)} #Pre-populate the slug field with the name field
    readonly_fields = ['created_at', 'updated_at', 'discount_percentage_display', 'sale_price'] #Exclude the fields from the admin interface
    
    fieldsets = ( #Organize the fields in the admin interface
        ('Basic Information', { #Organize the fields in the admin interface
            'fields': ('name', 'slug', 'sku', 'description', 'features') #Include the fields in the admin interface
        }),
        ('Categorization', { #Organize the fields in the admin interface
            'fields': ('category', 'subcategory', 'brand') #Include the fields in the admin interface
        }),
        ('Pricing', { #Organize the fields in the admin interface
            'fields': ('price', 'discount_percentage', 'sale_price', 'discount_percentage_display') #Include the fields in the admin interface
        }),
        ('Inventory', { #Organize the fields in the admin interface
            'fields': ('stock_quantity', 'min_stock_level') #Include the fields in the admin interface
        }),
        ('Media', { #Organize the fields in the admin interface
            'fields': ('main_image',) #Include the fields in the admin interface
        }),
        ('Status & Visibility', { #Organize the fields in the admin interface
            'fields': ('is_active', 'is_featured', 'is_bestseller') #Include the fields in the admin interface
        }),
        ('SEO & Marketing', { #Organize the fields in the admin interface
            'fields': ('meta_title', 'meta_description', 'keywords'), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
        ('Vendor Information', { #Organize the fields in the admin interface
            'fields': ('vendor', 'is_authentic_f1_part'), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
        ('Timestamps', { #Organize the fields in the admin interface
            'fields': ('created_at', 'updated_at'), #Include the fields in the admin interface
            'classes': ('collapse',) #Include the classes in the admin interface
        }),
    )

    def price_display(self, obj):
        """Display price with sale indicator"""
        if obj.is_on_sale: #Checks if the product is on sale
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">${}</span><br>' #Display the price with a line through
                '<span style="color: #e74c3c; font-weight: bold;">${}</span>', #Display the sale price
                obj.price, obj.sale_price #Display the price and sale price
            )
        return format_html('<span style="font-weight: bold;">${}</span>', obj.price) #Display the price
    price_display.short_description = 'Price' #Set the short description for the price field

    def stock_status_display(self, obj):
        """Display stock status with color coding"""
        status = obj.stock_status #Get the stock status
        if status == 'out_of_stock': #Check if the stock status is out of stock
            return format_html('<span style="color: #e74c3c; font-weight: bold;">Out of Stock</span>') #Display the stock status
        elif status == 'low_stock': #Check if the stock status is low stock
            return format_html('<span style="color: #f39c12; font-weight: bold;">Low Stock ({})</span>', obj.stock_quantity) #Display the stock status
        else:
            return format_html('<span style="color: #27ae60; font-weight: bold;">In Stock ({})</span>', obj.stock_quantity) #Display the stock status
    stock_status_display.short_description = 'Stock' #Set the short description for the stock status field

    def discount_percentage_display(self, obj):
        """Display discount percentage"""
        if obj.is_on_sale: #Checks if the product is on sale
            return format_html('<span style="color: #e74c3c; font-weight: bold;">{}% OFF</span>', obj.discount_percentage) #Display the discount percentage
        return "No discount" #Display the discount percentage
    discount_percentage_display.short_description = 'Discount' #Set the short description for the discount percentage field

    def get_queryset(self, request):
        """Optimize queryset with related fields"""
        return super().get_queryset(request).select_related('brand', 'category', 'subcategory') #Select the related fields

    actions = ['mark_featured', 'mark_bestseller', 'activate_products', 'deactivate_products'] #Display the actions in the admin interface

    def mark_featured(self, request, queryset):
        """Mark selected products as featured"""
        updated = queryset.update(is_featured=True) #Update the products
        self.message_user(request, f'{updated} products marked as featured.') #Display the message
    mark_featured.short_description = "Mark selected products as featured" #Set the short description for the mark featured field

    def mark_bestseller(self, request, queryset):
        """Mark selected products as bestsellers"""
        updated = queryset.update(is_bestseller=True) #Update the products
        self.message_user(request, f'{updated} products marked as bestsellers.') #Display the message
    mark_bestseller.short_description = "Mark selected products as bestsellers" #Set the short description for the mark bestseller field

    def activate_products(self, request, queryset):
        """Activate selected products"""
        updated = queryset.update(is_active=True) #Update the products
        self.message_user(request, f'{updated} products activated.') #Display the message
    activate_products.short_description = "Activate selected products" #Set the short description for the activate products field

    def deactivate_products(self, request, queryset):
        """Deactivate selected products"""
        updated = queryset.update(is_active=False) #Update the products
        self.message_user(request, f'{updated} products deactivated.') #Display the message
    deactivate_products.short_description = "Deactivate selected products" #Set the short description for the deactivate products field
