from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, ShippingMethod


class CartItemInline(admin.TabularInline):
    """
    Inline admin for cart items.
    """
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'updated_at']
    fields = ['product', 'quantity', 'total_price', 'added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Admin interface for shopping carts.
    """
    list_display = ['user', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]

    def total_items(self, obj):
        """Display total items in cart"""
        return obj.total_items
    total_items.short_description = 'Items'

    def total_price(self, obj):
        """Display total price"""
        return format_html('<span style="font-weight: bold;">${}</span>', obj.total_price)
    total_price.short_description = 'Total'


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for order items.
    """
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']
    fields = ['product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price']


class OrderStatusHistoryInline(admin.TabularInline):
    """
    Inline admin for order status history.
    """
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['changed_at']
    fields = ['status', 'notes', 'changed_by', 'changed_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for orders.
    Comprehensive order management with F1-inspired features.
    """
    list_display = [
        'order_number', 'user', 'order_status_display', 'payment_status_display', 
        'total_amount', 'created_at'
    ]
    list_filter = [
        'order_status', 'payment_status', 'created_at', 'shipped_at'
    ]
    search_fields = [
        'order_number', 'user__username', 'user__email', 
        'shipping_address', 'payment_transaction_id'
    ]
    readonly_fields = [
        'order_number', 'created_at', 'updated_at', 'shipped_at', 'delivered_at'
    ]
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'order_status', 'payment_status')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'discount_amount', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_address', 'shipping_city', 'shipping_state', 
                'shipping_postal_code', 'shipping_country', 'shipping_phone'
            )
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_transaction_id')
        }),
        ('Notes', {
            'fields': ('customer_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )

    def order_status_display(self, obj):
        """Display order status with color coding"""
        status_colors = {
            'pending': '#f39c12',
            'confirmed': '#3498db',
            'processing': '#9b59b6',
            'shipped': '#e67e22',
            'delivered': '#27ae60',
            'cancelled': '#e74c3c',
            'refunded': '#95a5a6'
        }
        color = status_colors.get(obj.order_status, '#000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_order_status_display()
        )
    order_status_display.short_description = 'Order Status'

    def payment_status_display(self, obj):
        """Display payment status with color coding"""
        if obj.payment_status == 'paid':
            return format_html('<span style="color: #27ae60; font-weight: bold;">✓ Paid</span>')
        elif obj.payment_status == 'failed':
            return format_html('<span style="color: #e74c3c; font-weight: bold;">✗ Failed</span>')
        else:
            return format_html('<span style="color: #f39c12; font-weight: bold;">⏳ Pending</span>')
    payment_status_display.short_description = 'Payment'

    def total_amount(self, obj):
        """Display total amount with formatting"""
        return format_html('<span style="font-weight: bold; color: #e74c3c;">${}</span>', obj.total_amount)
    total_amount.short_description = 'Total'

    actions = [
        'mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 
        'mark_as_delivered', 'mark_as_cancelled', 'mark_as_paid'
    ]

    def mark_as_confirmed(self, request, queryset):
        """Mark selected orders as confirmed"""
        updated = queryset.update(order_status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected orders as confirmed"

    def mark_as_processing(self, request, queryset):
        """Mark selected orders as processing"""
        updated = queryset.update(order_status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = "Mark selected orders as processing"

    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as shipped"""
        from django.utils import timezone
        updated = queryset.update(order_status='shipped', shipped_at=timezone.now())
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = "Mark selected orders as shipped"

    def mark_as_delivered(self, request, queryset):
        """Mark selected orders as delivered"""
        from django.utils import timezone
        updated = queryset.update(order_status='delivered', delivered_at=timezone.now())
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as delivered"

    def mark_as_cancelled(self, request, queryset):
        """Mark selected orders as cancelled"""
        updated = queryset.update(order_status='cancelled')
        self.message_user(request, f'{updated} orders marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected orders as cancelled"

    def mark_as_paid(self, request, queryset):
        """Mark selected orders as paid"""
        updated = queryset.update(payment_status='paid')
        self.message_user(request, f'{updated} orders marked as paid.')
    mark_as_paid.short_description = "Mark selected orders as paid"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for order items.
    """
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'total_price']
    list_filter = ['order__order_status']
    search_fields = ['order__order_number', 'product_name', 'product_sku']
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for order status history.
    """
    list_display = ['order', 'status', 'changed_by', 'changed_at']
    list_filter = ['status', 'changed_at']
    search_fields = ['order__order_number', 'changed_by__username']
    readonly_fields = ['changed_at']
    ordering = ['-changed_at']


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    """
    Admin interface for shipping methods.
    """
    list_display = ['name', 'cost', 'estimated_days', 'is_active']
    list_filter = ['is_active', 'estimated_days']
    search_fields = ['name', 'description']
    ordering = ['name']
