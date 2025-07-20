from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
import os
from decimal import Decimal
import re
import random
import string


def validate_file_size(value): #Validates the file size
    # check file size
    filesize = value.size #Gets the file size
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("File size cannot exceed 5MB") #Raises an error if the file size is greater than 5MB

def validate_file_type(value): #Validates the file type
    # check file type
    ext = os.path.splitext(value.name)[1] #Gets the extension of the file
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'] #Sets the valid extensions to JPG, JPEG, PNG, GIF and WebP
    if not ext.lower() in valid_extensions: #Checks if the extension is not in the valid extensions
        raise ValidationError('Only image files are allowed.') #Raises an error if the extension is not in the valid extensions

def validate_product_name(value):
    """Validate product name - no special characters except basic punctuation"""
    if len(value.strip()) < 3: #Checks if the product name is less than 3 characters
        raise ValidationError('Product name must be at least 3 characters long.') #Raises an error if the product name is less than 3 characters
    
    # Check for potentially harmful characters
    harmful_pattern = r'[<>"\']' #Sets the harmful pattern to <, >, ", or '
    if re.search(harmful_pattern, value): #Checks if the product name contains the harmful pattern
        raise ValidationError('Product name cannot contain <, >, ", or \' characters.') #Raises an error if the product name contains the harmful pattern
    
    # Check for excessive spaces
    if '  ' in value: #Checks if the product name contains multiple consecutive spaces
        raise ValidationError('Product name cannot contain multiple consecutive spaces.') #Raises an error if the product name contains multiple consecutive spaces
    
    return value.strip()

def validate_product_description(value):
    """Validate product description"""
    if len(value.strip()) < 10: #Checks if the product description is less than 10 characters
        raise ValidationError('Product description must be at least 10 characters long.') #Raises an error if the product description is less than 10 characters
    
    # Check for potentially harmful characters
    harmful_pattern = r'<script|javascript:|vbscript:|onload=|onerror=' #Sets the harmful pattern to <script, javascript:, vbscript:, onload=, or onerror=
    if re.search(harmful_pattern, value, re.IGNORECASE): #Checks if the product description contains the harmful pattern
        raise ValidationError('Product description contains invalid content.') #Raises an error if the product description contains the harmful pattern
    
    return value.strip()

def validate_sku(value):
    """Validate SKU format"""
    if not value:  # Allow empty values for auto-generation
        return value
    
    if len(value.strip()) < 3: #Checks if the SKU is less than 3 characters
        raise ValidationError('SKU must be at least 3 characters long.') #Raises an error if the SKU is less than 3 characters
    
    # Allow alphanumeric characters, hyphens, and underscores only
    if not re.match(r'^[A-Za-z0-9_-]+$', value): #Checks if the SKU contains only alphanumeric characters, hyphens, and underscores
        raise ValidationError('SKU can only contain letters, numbers, hyphens, and underscores.') #Raises an error if the SKU contains only alphanumeric characters, hyphens, and underscores
    
    return value.strip().upper()

def validate_price(value):
    """Validate price - must be positive and reasonable"""
    if value <= 0: #Checks if the price is less than or equal to 0
        raise ValidationError('Price must be greater than 0.') #Raises an error if the price is less than or equal to 0
    
    if value > 999999.99: #Checks if the price is greater than 999999.99
        raise ValidationError('Price cannot exceed $999,999.99.') #Raises an error if the price is greater than 999999.99
    
    return value

def validate_stock_quantity(value):
    """Validate stock quantity"""
    if value < 0: #Checks if the stock quantity is less than 0
        raise ValidationError('Stock quantity cannot be negative.') #Raises an error if the stock quantity is less than 0
    
    if value > 999999: #Checks if the stock quantity is greater than 999999
        raise ValidationError('Stock quantity cannot exceed 999,999.') #Raises an error if the stock quantity is greater than 999999
    
    return value


class Category(models.Model):
    # Product categories
    name = models.CharField(max_length=100, unique=True) #Sets the name of the category
    slug = models.SlugField(max_length=100, unique=True, blank=True) #Sets the slug of the category
    description = models.TextField(blank=True) #Sets the description of the category
    image = models.ImageField(upload_to='categories/', blank=True, null=True, validators=[validate_file_size, validate_file_type]) #Sets the image of the category
    icon_class = models.ImageField(upload_to='categories/', max_length=50, blank=True, help_text="CSS class for category icon") #Sets the icon class of the category
    is_active = models.BooleanField(default=True) #Sets the active status of the category
    created_at = models.DateTimeField(auto_now_add=True) #Sets the created at of the category
    updated_at = models.DateTimeField(auto_now=True) #Sets the updated at of the category

    class Meta:
        verbose_name_plural = "Categories" #Sets the verbose name of the category
        ordering = ['name'] #Sets the ordering of the category

    def __str__(self):
        return self.name #Returns the name of the category

    def save(self, *args, **kwargs):
        # auto create slug
        if not self.slug: #Checks if the slug is not set
            self.slug = slugify(self.name) #Sets the slug of the category
        super().save(*args, **kwargs) #Saves the category

    def get_absolute_url(self):
        # get category url
        return reverse('products:category_detail', kwargs={'slug': self.slug}) #Returns the absolute url of the category


class SubCategory(models.Model):
    # Subcategories
    name = models.CharField(max_length=100) #Sets the name of the subcategory
    slug = models.SlugField(max_length=100, blank=True) #Sets the slug of the subcategory
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories') #Sets the category of the subcategory
    description = models.TextField(blank=True) #Sets the description of the subcategory
    is_active = models.BooleanField(default=True) #Sets the active status of the subcategory
    created_at = models.DateTimeField(auto_now_add=True) #Sets the created at of the subcategory

    class Meta:
        verbose_name_plural = "Sub Categories" #Sets the verbose name of the subcategory
        unique_together = ['name', 'category'] #Sets the unique together of the subcategory
        ordering = ['category', 'name'] #Sets the ordering of the subcategory

    def __str__(self):
        return f"{self.category.name} - {self.name}" #Returns the name of the subcategory

    def save(self, *args, **kwargs):
        # auto create slug
        if not self.slug: #Checks if the slug is not set
            self.slug = slugify(self.name) #Sets the slug of the subcategory
        super().save(*args, **kwargs) #Saves the subcategory

    def get_absolute_url(self):
        # get subcategory url
        return reverse('products:subcategory_detail', kwargs={'category_slug': self.category.slug, 'subcategory_slug': self.slug})


class Brand(models.Model):
    # Car parts brands
    name = models.CharField(max_length=100, unique=True) #Sets the name of the brand
    slug = models.SlugField(max_length=100, unique=True, blank=True) #Sets the slug of the brand
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, validators=[validate_file_size, validate_file_type]) #Sets the logo of the brand
    description = models.TextField(blank=True) #Sets the description of the brand
    website = models.URLField(blank=True) #Sets the website of the brand
    is_f1_team = models.BooleanField(default=False, help_text="Is this an F1 team brand?") #Sets the F1 team status of the brand
    is_active = models.BooleanField(default=True) #Sets the active status of the brand
    created_at = models.DateTimeField(auto_now_add=True) #Sets the created at of the brand

    class Meta:
        ordering = ['name'] #Sets the ordering of the brand

    def __str__(self):
        return self.name #Returns the name of the brand

    def save(self, *args, **kwargs):
        # auto create slug
        if not self.slug: #Checks if the slug is not set
            self.slug = slugify(self.name) #Sets the slug of the brand
        super().save(*args, **kwargs) #Saves the brand


class Product(models.Model):
    # Main product model
    # Basic Information
    name = models.CharField(
        max_length=40, 
        # validators=[validate_product_name],  # Temporarily disabled for testing
        help_text="Product name (max 40 characters)"
    ) #Sets the name of the product
    slug = models.SlugField(max_length=200, blank=True) #Sets the slug of the product
    sku = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True,
        validators=[validate_sku],
        help_text="Stock Keeping Unit (auto-generated if not provided)"
    ) #Sets the SKU of the product

    # Categorization
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products') #Sets the category of the product
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products') #Sets the subcategory of the product
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products') #Sets the brand of the product

    # Pricing
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[validate_price]
    ) #Sets the price of the product
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #Sets the sale price of the product
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)], help_text="Discount percentage (0-100)") #Sets the discount percentage of the product

    # Inventory
    stock_quantity = models.PositiveIntegerField(
        default=0, #Sets the default stock quantity to 0
        validators=[validate_stock_quantity] #Validates the stock quantity
    ) #Sets the stock quantity of the product
    min_stock_level = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(1000)]) #Sets the minimum stock level of the product

    # Product Details
    description = models.TextField(
        max_length=1200, 
        # validators=[validate_product_description],  # Temporarily disabled for testing
        help_text="Product description (max 1200 characters)"
    ) #Sets the description of the product
    features = models.TextField(
        blank=True, 
        max_length=1000, 
        help_text="Key features and benefits (max 1000 characters)"
    ) #Sets the features of the product

    # Images
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True, validators=[validate_file_size, validate_file_type]) #Sets the main image of the product

    # Status and Visibility
    is_active = models.BooleanField(default=True) #Sets the active status of the product
    is_featured = models.BooleanField(default=False) #Sets the featured status of the product
    is_bestseller = models.BooleanField(default=False) #Sets the bestseller status of the product

    # SEO and Marketing
    meta_title = models.CharField(max_length=200, blank=True) #Sets the meta title of the product
    meta_description = models.TextField(blank=True) #Sets the meta description of the product
    keywords = models.CharField(max_length=500, blank=True) #Sets the keywords of the product

    # Vendor Information
    vendor = models.ForeignKey( #Sets the vendor of the product
        'users.UserProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='vendor_products',
        help_text="Vendor who created this product"
    )
    is_authentic_f1_part = models.BooleanField( #Sets the authentic F1 part status of the product
        default=False,
        help_text="Is this an authentic F1 part from a verified vendor?"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True) #Sets the created at of the product
    updated_at = models.DateTimeField(auto_now=True) #Sets the updated at of the product

    class Meta:
        ordering = ['-created_at'] #Sets the ordering of the product

    def __str__(self):
        return f"{self.brand.name} - {self.name}" #Returns the name of the product

    def generate_sku(self):
        """Generate SKU based on brand, category, and random numbers"""
        # Get first 3 letters of brand name (uppercase)
        brand_prefix = self.brand.name[:3].upper()
        
        # Get first 3 letters of category name (uppercase)
        category_prefix = self.category.name[:3].upper()
        
        # Generate 4 random digits
        random_digits = ''.join(random.choices(string.digits, k=4))
        
        # Check if product is created by a vendor
        if self.vendor:
            sku = f"VENDOR-{brand_prefix}-{category_prefix}-{random_digits}"
        else:
            sku = f"{brand_prefix}-{category_prefix}-{random_digits}"
        
        return sku

    def save(self, *args, **kwargs):
        # Auto-generate SKU if not provided
        if not self.sku:
            # Generate SKU and ensure it's unique
            max_attempts = 10
            for attempt in range(max_attempts):
                generated_sku = self.generate_sku()
                if not Product.objects.filter(sku=generated_sku).exists():
                    self.sku = generated_sku
                    break
                if attempt == max_attempts - 1:
                    # If we can't generate a unique SKU, add a random suffix
                    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
                    self.sku = f"{generated_sku}-{random_suffix}"
        
        # Auto-calculate sale_price from price and discount_percentage
        if self.discount_percentage: #Checks if the discount percentage is set
            self.sale_price = self.price * (Decimal('1') - Decimal(self.discount_percentage) / Decimal('100')) #Calculates the sale price
            if self.discount_percentage == 0: #Checks if the discount percentage is 0
                self.sale_price = None #Sets the sale price to None
        else: #If the discount percentage is not set
            self.sale_price = None #Sets the sale price to None
        if not self.slug: #Checks if the slug is not set
            self.slug = slugify(self.name) #Sets the slug of the product
        super().save(*args, **kwargs) #Saves the product

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug}) #Returns the absolute url of the product

    @property
    def is_on_sale(self):
        # Check if product is on sale
        return self.sale_price is not None and self.sale_price < self.price #Checks if the product is on sale

    @property
    def current_price(self):
        # Get current price
        return self.sale_price if self.is_on_sale else self.price #Returns the current price

    @property
    def stock_status(self):
        # Get stock status
        if self.stock_quantity == 0: #Checks if the stock quantity is 0
            return 'out_of_stock' #Returns the stock status as out of stock
        elif self.stock_quantity <= self.min_stock_level: #Checks if the stock quantity is less than or equal to the minimum stock level
            return 'low_stock' #Returns the stock status as low stock
        else:
            return 'in_stock' #Returns the stock status as in stock

    @property
    def average_rating(self):
        # Get average rating
        ratings = self.ratings.all() #Gets all the ratings for the product
        if ratings.exists(): #Checks if the ratings exist
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 1) #Returns the average rating
        return None #Returns None


class ProductRating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings') #Sets the product of the rating
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #Sets the user of the rating
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)]) #Sets the rating of the product
    created_at = models.DateTimeField(auto_now_add=True) #Sets the created at of the rating

    class Meta:
        unique_together = ('product', 'user') #Sets the unique together of the rating

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} {self.rating}/5" #Returns the rating of the product



