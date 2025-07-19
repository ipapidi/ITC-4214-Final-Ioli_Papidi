from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cart(models.Model):
    # Shopping cart
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart') #One to one relationship with the User model
    created_at = models.DateTimeField(auto_now_add=True) #Automatically adds the current date and time when the object is created
    updated_at = models.DateTimeField(auto_now=True) #Automatically adds the current date and time when the object is updated

    def __str__(self):
        return f"Cart for {self.user.username}" #Returns the username of the user

    @property
    def total_items(self):
        # Get total number of items in cart
        return sum(item.quantity for item in self.items.all()) #Returns the total number of items in the cart

    @property
    def total_price(self):
        # Calculate total price
        return sum(item.total_price for item in self.items.all()) #Returns the total price of the items in the cart

    @property
    def total_price_with_tax(self):
        # Calculate total price with tax
        tax_rate = Decimal('0.24')  # 24% tax rate to match Order model
        return self.total_price + (self.total_price * tax_rate) #Returns the total price of the items in the cart with tax



class CartItem(models.Model):
    # Cart items
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') #One to many relationship with the Cart model
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE) #One to many relationship with the Product model
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)]) #Positive integer field with a default value of 1 and a minimum value of 1
    added_at = models.DateTimeField(auto_now_add=True) #Automatically adds the current date and time when the object is created
    updated_at = models.DateTimeField(auto_now=True) #Automatically adds the current date and time when the object is updated

    class Meta:
        unique_together = ['cart', 'product'] #Ensures that the cart and product are unique together

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.cart.user.username}'s cart" #Returns the quantity of the product in the cart

    @property
    def total_price(self):
        # Calculate total price for this item
        return self.product.current_price * self.quantity #Returns the total price of the item

    def save(self, *args, **kwargs):
        # Ensure quantity doesn't exceed available stock
        if self.quantity > self.product.stock_quantity: #Checks if the quantity is greater than the stock quantity
            self.quantity = self.product.stock_quantity #Sets the quantity to the stock quantity
        super().save(*args, **kwargs) #Saves the object


class Order(models.Model):
    # Order model
    ORDER_STATUS_CHOICES = [ #Choices for the order status
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [ #Choices for the payment status
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    # Order Information
    order_number = models.CharField(max_length=20, unique=True) #Unique order number
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders') #One to many relationship with the User model

    # Status
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending') #Choices for the order status
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending') #Choices for the payment status

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2) #Subtotal of the order
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) #Tax amount of the order
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0) #Shipping cost of the order
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) #Discount amount of the order
    total_amount = models.DecimalField(max_digits=10, decimal_places=2) #Total amount of the order

    # Shipping Information
    shipping_address = models.TextField() #Shipping address of the order
    shipping_city = models.CharField(max_length=100) #Shipping city of the order
    shipping_state = models.CharField(max_length=100) #Shipping state of the order
    shipping_postal_code = models.CharField(max_length=20) #Shipping postal code of the order
    shipping_country = models.CharField(max_length=100) #Shipping country of the order
    shipping_phone = models.CharField(max_length=20) #Shipping phone of the order

    # Payment Information (simulated)
    payment_method = models.CharField(max_length=50, default='Credit Card') #Payment method of the order
    payment_transaction_id = models.CharField(max_length=100, blank=True) #Payment transaction id of the order

    # Notes
    customer_notes = models.TextField(blank=True) #Customer notes of the order
    admin_notes = models.TextField(blank=True) #Admin notes of the order

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True) #Automatically adds the current date and time when the object is created
    updated_at = models.DateTimeField(auto_now=True) #Automatically adds the current date and time when the object is updated
    shipped_at = models.DateTimeField(blank=True, null=True) #Shipped at of the order
    delivered_at = models.DateTimeField(blank=True, null=True) #Delivered at of the order

    class Meta:
        ordering = ['-created_at'] #Orders the objects by the created at field

    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}" #Returns the order number and username of the user

    def save(self, *args, **kwargs): #Saves the object
        if not self.order_number:
            # Generate order number: RF-YYYYMMDD-XXXX
            from datetime import datetime #Imports the datetime module
            date_str = datetime.now().strftime('%Y%m%d') #Formats the date as YYYYMMDD
            last_order = Order.objects.filter(order_number__startswith=f'RF-{date_str}').order_by('-order_number').first() #Filters the objects by the order number

            if last_order:
                last_number = int(last_order.order_number.split('-')[-1]) #Splits the order number and gets the last number
                new_number = last_number + 1 #Adds 1 to the last number
            else:
                new_number = 1 #Sets the new number to 1

            self.order_number = f"RF-{date_str}-{new_number:04d}" #Formats the order number as RF-YYYYMMDD-XXXX

        super().save(*args, **kwargs) #Saves the object

    @property
    def is_paid(self):
        # Check if order is paid
        return self.payment_status == 'paid' #Checks if the payment status is paid

    @property
    def can_cancel(self):
        # Check if order can be cancelled
        return self.order_status in ['pending', 'confirmed'] #Checks if the order status is pending or confirmed

    def calculate_totals(self):
        # Calculate order totals
        from decimal import Decimal
        subtotal = sum(item.total_price for item in self.items.all()) #Calculates the subtotal
        tax_amount = subtotal * Decimal('0.24')  #Calculates the tax amount (24% tax)
        total = subtotal + tax_amount + self.shipping_cost - self.discount_amount #Calculates the total

        self.subtotal = subtotal #Sets the subtotal
        self.tax_amount = tax_amount #Sets the tax amount
        self.total_amount = total #Sets the total
        self.save() #Saves the object


class OrderItem(models.Model):
    # Order items
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items') #One to many relationship with the Order model
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE) #One to many relationship with the Product model
    product_name = models.CharField(max_length=200)  # Snapshot of product name
    product_sku = models.CharField(max_length=50)    # Snapshot of product SKU
    quantity = models.PositiveIntegerField() #Quantity of the product
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) #Unit price of the product
    total_price = models.DecimalField(max_digits=10, decimal_places=2) #Total price of the product

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in Order {self.order.order_number}" #Returns the quantity of the product in the order

    def save(self, *args, **kwargs):
        if not self.product_name:
            self.product_name = self.product.name #Sets the product name
        if not self.product_sku:
            self.product_sku = self.product.sku #Sets the product SKU
        if not self.unit_price:
            self.unit_price = self.product.current_price #Sets the unit price
        if not self.total_price:
            self.total_price = self.unit_price * self.quantity #Sets the total price

        super().save(*args, **kwargs) #Saves the object



class OrderStatusHistory(models.Model):
    # Order status history
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history') #One to many relationship with the Order model
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES) #Choices for the order status
    notes = models.TextField(blank=True) #Notes of the order
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #One to many relationship with the User model
    changed_at = models.DateTimeField(auto_now_add=True) #Automatically adds the current date and time when the object is created

    class Meta:
        ordering = ['-changed_at'] #Orders the objects by the changed at field

    def __str__(self):
        return f"Order {self.order.order_number} - {self.status} at {self.changed_at}" #Returns the order number, status and changed at


class ShippingMethod(models.Model):
    # Shipping methods
    name = models.CharField(max_length=100) #Name of the shipping method
    description = models.TextField(blank=True) #Description of the shipping method
    cost = models.DecimalField(max_digits=10, decimal_places=2) #Cost of the shipping method
    estimated_days = models.PositiveIntegerField(help_text="Estimated delivery time in days") #Estimated delivery time in days
    is_active = models.BooleanField(default=True) #Is the shipping method active

    def __str__(self):
        return f"{self.name} - ${self.cost} ({self.estimated_days} days)" #Returns the name, cost and estimated delivery time


class PaymentMethod(models.Model):
    # payment methods
    name = models.CharField(max_length=100) #Name of the payment method
    description = models.TextField(blank=True) #Description of the payment method
    is_active = models.BooleanField(default=True) #Is the payment method active
    requires_card_info = models.BooleanField(default=False, help_text="Does this method require card details?") #Does the payment method require card details?

    def __str__(self):
        return self.name
