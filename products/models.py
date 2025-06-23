from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """
    Main product categories for car performance parts.
    F1-inspired categories like Engine, Aerodynamics, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    icon_class = models.CharField(max_length=50, blank=True, help_text="CSS class for category icon")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:category_detail', kwargs={'slug': self.slug})


class SubCategory(models.Model):
    """
    Sub-categories within main categories.
    Example: Engine -> Turbochargers, Exhaust Systems, etc.
    """
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
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:subcategory_detail', kwargs={'category_slug': self.category.slug, 'subcategory_slug': self.slug})


class Brand(models.Model):
    """
    Car parts brands/manufacturers.
    Includes both F1 teams and aftermarket brands.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
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
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Main product model for car performance parts.
    Includes comprehensive details for F1-inspired parts.
    """
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
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    min_stock_level = models.PositiveIntegerField(default=5)
    
    # Product Details
    description = models.TextField()
    specifications = models.JSONField(default=dict, blank=True, help_text="Technical specifications as JSON")
    features = models.TextField(blank=True, help_text="Key features and benefits")
    
    # Images
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True)
    
    # Performance Metrics (F1-inspired)
    performance_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Performance rating from 1-10"
    )
    weight_savings = models.CharField(max_length=50, blank=True, help_text="e.g., '2.5kg lighter'")
    power_gain = models.CharField(max_length=50, blank=True, help_text="e.g., '+25 HP'")
    
    # Compatibility
    compatible_cars = models.TextField(blank=True, help_text="Compatible car models")
    installation_difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
            ('expert', 'Expert Only')
        ],
        default='medium'
    )
    
    # Status and Visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    
    # SEO and Marketing
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    keywords = models.CharField(max_length=500, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    @property
    def is_on_sale(self):
        """Check if product is on sale"""
        return self.sale_price is not None and self.sale_price < self.price

    @property
    def current_price(self):
        """Get current price (sale price if available, otherwise regular price)"""
        return self.sale_price if self.is_on_sale else self.price

    @property
    def discount_percentage(self):
        """Calculate discount percentage if on sale"""
        if self.is_on_sale:
            return int(((self.price - self.sale_price) / self.price) * 100)
        return 0

    @property
    def stock_status(self):
        """Get stock status for display"""
        if self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.stock_quantity <= self.min_stock_level:
            return 'low_stock'
        else:
            return 'in_stock'


class ProductImage(models.Model):
    """
    Additional images for products.
    Allows multiple images per product for detailed views.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/additional/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductSpecification(models.Model):
    """
    Detailed specifications for products.
    Allows flexible specification structure for different product types.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ['product', 'name']

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value} {self.unit}".strip()
