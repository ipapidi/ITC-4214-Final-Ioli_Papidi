from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
import os
from decimal import Decimal


def validate_file_size(value):
    # check file size
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB limit
        raise ValidationError("File size cannot exceed 5MB")

def validate_file_type(value):
    # check file type
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Only image files are allowed.')


class Category(models.Model):
    # Product categories
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True, validators=[validate_file_size, validate_file_type])
    icon_class = models.ImageField(upload_to='categories/', max_length=50, blank=True, help_text="CSS class for category icon")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # auto create slug
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # get category url
        return reverse('products:category_detail', kwargs={'slug': self.slug})


class SubCategory(models.Model):
    # Subcategories
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Sub Categories"
        unique_together = ['name', 'category']
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        # auto create slug
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # get subcategory url
        return reverse('products:subcategory_detail', kwargs={'category_slug': self.category.slug, 'subcategory_slug': self.slug})


class Brand(models.Model):
    # Car parts brands
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, validators=[validate_file_size, validate_file_type])
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_f1_team = models.BooleanField(default=False, help_text="Is this an F1 team brand?")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # auto create slug
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    # Main product model
    # Basic Information
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")

    # Categorization
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)], help_text="Discount percentage (0-100)")

    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)

    # Product Details
    description = models.TextField()
    features = models.TextField(blank=True, help_text="Key features and benefits")

    # Images
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True, validators=[validate_file_size, validate_file_type])

    # Status and Visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)

    # SEO and Marketing
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)

    # Vendor Information
    vendor = models.ForeignKey(
        'users.UserProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='vendor_products',
        help_text="Vendor who created this product"
    )
    is_authentic_f1_part = models.BooleanField(
        default=False,
        help_text="Is this an authentic F1 part from a verified vendor?"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    def save(self, *args, **kwargs):
        # Auto-calculate sale_price from price and discount_percentage
        if self.discount_percentage:
            self.sale_price = self.price * (Decimal('1') - Decimal(self.discount_percentage) / Decimal('100'))
            if self.discount_percentage == 0:
                self.sale_price = None
        else:
            self.sale_price = None
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    @property
    def is_on_sale(self):
        # Check if product is on sale
        return self.sale_price is not None and self.sale_price < self.price

    @property
    def current_price(self):
        # Get current price
        return self.sale_price if self.is_on_sale else self.price

    @property
    def stock_status(self):
        # Get stock status
        if self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.stock_quantity <= self.min_stock_level:
            return 'low_stock'
        else:
            return 'in_stock'

    @property
    def average_rating(self):
        # Get average rating
        ratings = self.ratings.all()
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return None


class ProductRating(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} {self.rating}/5"
