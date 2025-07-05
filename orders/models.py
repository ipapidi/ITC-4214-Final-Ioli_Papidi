from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cart(models.Model):
    # Shopping cart
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_items(self):
        # Get total number of items in cart
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        # Calculate total price
        return sum(item.total_price for item in self.items.all())

    @property
    def total_price_with_tax(self):
        # Calculate total price with tax
        tax_rate = Decimal('0.08')  # 8% tax rate
        return self.total_price + (self.total_price * tax_rate)


class CartItem(models.Model):
    # Cart items
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.cart.user.username}'s cart"

    @property
    def total_price(self):
        # Calculate total price for this item
        return self.product.current_price * self.quantity

    def save(self, *args, **kwargs):
        # Ensure quantity doesn't exceed available stock
        if self.quantity > self.product.stock_quantity:
            self.quantity = self.product.stock_quantity
        super().save(*args, **kwargs)


class Order(models.Model):
    # Order model
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # Order Information
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    # Status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Shipping Information
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20)
    
    # Payment Information (simulated)
    payment_method = models.CharField(max_length=50, default='Credit Card')
    payment_transaction_id = models.CharField(max_length=100, blank=True)
    
    # Notes
    customer_notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number: RF-YYYYMMDD-XXXX
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=f'RF-{date_str}').order_by('-order_number').first()
            
            if last_order:
                last_number = int(last_order.order_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.order_number = f"RF-{date_str}-{new_number:04d}"
        
        super().save(*args, **kwargs)

    @property
    def is_paid(self):
        # Check if order is paid
        return self.payment_status == 'paid'

    @property
    def can_cancel(self):
        # Check if order can be cancelled
        return self.order_status in ['pending', 'confirmed']

    def calculate_totals(self):
        # Calculate order totals
        subtotal = sum(item.total_price for item in self.items.all())
        tax_amount = subtotal * Decimal('0.08')  # 8% tax
        total = subtotal + tax_amount + self.shipping_cost - self.discount_amount
        
        self.subtotal = subtotal
        self.tax_amount = tax_amount
        self.total_amount = total
        self.save()


class OrderItem(models.Model):
    # Order items
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)  # Snapshot of product name
    product_sku = models.CharField(max_length=50)    # Snapshot of product SKU
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Product snapshot (in case product is deleted)
    product_snapshot = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order {self.order.order_number}"

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_sku:
            self.product_sku = self.product.sku
        if not self.unit_price:
            self.unit_price = self.product.current_price
        if not self.total_price:
            self.total_price = self.unit_price * self.quantity
        
        # Create product snapshot
        self.product_snapshot = {
            'name': self.product.name,
            'sku': self.product.sku,
            'brand': self.product.brand.name,
            'category': self.product.category.name,
            'specifications': self.product.specifications,
        }
        
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    # Order status history
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    notes = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"Order {self.order.order_number} - {self.status} at {self.changed_at}"


class ShippingMethod(models.Model):
    # Shipping methods
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_days = models.PositiveIntegerField(help_text="Estimated delivery time in days")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ${self.cost} ({self.estimated_days} days)"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    requires_card_info = models.BooleanField(default=False, help_text="Does this method require card details?")

    def __str__(self):
        return self.name
