from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, ShippingMethod, PaymentMethod


class CartItemInline(admin.TabularInline):
    """
    Inline admin for cart items.
    """
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'updated_at'] #Excludes the fields from the admin interface
    fields = ['product', 'quantity', 'total_price', 'added_at'] #Includes the fields in the admin interface


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin): 
    """
    Admin interface for shopping carts.
    """
    list_display = ['user', 'total_items', 'total_price', 'created_at'] #Display the fields in the admin interface
    list_filter = ['created_at'] #Filter the fields in the admin interface
    search_fields = ['user__username', 'user__email'] #Search the fields in the admin interface
    readonly_fields = ['created_at', 'updated_at'] #Excludes the fields from the admin interface
    inlines = [CartItemInline] #Includes the inline admin for cart items

    def total_items(self, obj): 
        """Display total items in cart"""
        return obj.total_items #Returns the total items in the cart
    total_items.short_description = 'Items' #Sets the short description for the total items field

    def total_price(self, obj):
        """Display total price"""
        return format_html('<span style="font-weight: bold;">${}</span>', obj.total_price)
    total_price.short_description = 'Total' #Sets the short description for the total price field


class OrderItemInline(admin.TabularInline):
    """
    Inline admin for order items.
    """
    model = OrderItem #The model to be used for the inline admin
    extra = 0 #The number of extra forms to display
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price'] #Excludes the fields from the admin interface
    fields = ['product', 'product_name', 'product_sku', 'quantity', 'unit_price', 'total_price'] #Includes the fields in the admin interface


class OrderStatusHistoryInline(admin.TabularInline):
    """
    Inline admin for order status history.
    """
    model = OrderStatusHistory #The model to be used for the inline admin
    extra = 0 #The number of extra forms to display
    readonly_fields = ['changed_at'] #Excludes the fields from the admin interface
    fields = ['status', 'notes', 'changed_by', 'changed_at'] #Includes the fields in the admin interface


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin interface for orders.
    Comprehensive order management with F1-inspired features.
    """
    list_display = [ #Display the fields in the admin interface
        'order_number', 'user', 'order_status_display', 'payment_status_display', 
        'total_amount', 'created_at' #Includes the fields in the admin interface
    ]
    list_filter = [ #Filter the fields in the admin interface
        'order_status', 'payment_status', 'created_at', 'shipped_at'
    ]
    search_fields = [ #Search the fields in the admin interface
        'order_number', 'user__username', 'user__email', 
        'shipping_address', 'payment_transaction_id' #Includes the fields in the admin interface
    ]
    readonly_fields = [ #Excludes the fields from the admin interface
        'order_number', 'created_at', 'updated_at', 'shipped_at', 'delivered_at'
    ]
    inlines = [OrderItemInline, OrderStatusHistoryInline] #Includes the inline admin for order items and order status history
    
    fieldsets = ( #Organizes the fields in the admin interface
        ('Order Information', { #Organizes the fields in the admin interface
            'fields': ('order_number', 'user', 'order_status', 'payment_status') #Includes the fields in the admin interface
        }),
        ('Pricing', { #Organizes the fields in the admin interface
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'discount_amount', 'total_amount') #Includes the fields in the admin interface
        }),
        ('Shipping Information', { #Organizes the fields in the admin interface
            'fields': ( #Includes the fields in the admin interface
                'shipping_address', 'shipping_city', 'shipping_state', 
                'shipping_postal_code', 'shipping_country', 'shipping_phone' #Includes the fields in the admin interface
            )
        }),
        ('Payment Information', { #Organizes the fields in the admin interface
            'fields': ('payment_method', 'payment_transaction_id') #Includes the fields in the admin interface
        }),
        ('Notes', { #Organizes the fields in the admin interface
            'fields': ('customer_notes', 'admin_notes') #Includes the fields in the admin interface
        }),
        ('Timestamps', { #Organizes the fields in the admin interface
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'), #Includes the fields in the admin interface
            'classes': ('collapse',) #
        }),
    )

    def order_status_display(self, obj):
        """Display order status with color coding"""
        status_colors = { #Defines the status colors
            'pending': '#f39c12',
            'confirmed': '#3498db',
            'processing': '#9b59b6',
            'shipped': '#e67e22',
            'delivered': '#27ae60',
            'cancelled': '#e74c3c',
            'refunded': '#95a5a6'
        }
        color = status_colors.get(obj.order_status, '#000') #Gets the color for the order status
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_order_status_display() #Displays the order status with the color
        )
    order_status_display.short_description = 'Order Status' #Sets the short description for the order status field

    def payment_status_display(self, obj):
        """Display payment status with color coding"""
        if obj.payment_status == 'paid': #Checks if the payment status is paid
            return format_html('<span style="color: #27ae60; font-weight: bold;">✓ Paid</span>') #Displays the payment status with the color
        elif obj.payment_status == 'failed': #Checks if the payment status is failed
            return format_html('<span style="color: #e74c3c; font-weight: bold;">✗ Failed</span>')
        else:
            return format_html('<span style="color: #f39c12; font-weight: bold;">⏳ Pending</span>') #Displays the payment status with the color
    payment_status_display.short_description = 'Payment' #Sets the short description for the payment status field

    def total_amount(self, obj):
        """Display total amount with formatting"""
        return format_html('<span style="font-weight: bold; color: #e74c3c;">${}</span>', obj.total_amount) #Displays the total amount with the color
    total_amount.short_description = 'Total' #Sets the short description for the total amount field

    actions = [ #Includes the actions in the admin interface
        'mark_as_confirmed', 'mark_as_processing', 'mark_as_shipped', 
        'mark_as_delivered', 'mark_as_cancelled', 'mark_as_paid' #Includes the actions in the admin interface
    ]

    def mark_as_confirmed(self, request, queryset):
        """Mark selected orders as confirmed"""
        updated = queryset.update(order_status='confirmed') #Updates the order status to confirmed
        self.message_user(request, f'{updated} orders marked as confirmed.') #Displays the message
    mark_as_confirmed.short_description = "Mark selected orders as confirmed" #Sets the short description for the mark as confirmed action

    def mark_as_processing(self, request, queryset):
        """Mark selected orders as processing"""
        updated = queryset.update(order_status='processing') #Updates the order status to processing
        self.message_user(request, f'{updated} orders marked as processing.') #Displays the message
    mark_as_processing.short_description = "Mark selected orders as processing" #Sets the short description for the mark as processing action

    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as shipped"""
        from django.utils import timezone #Imports the timezone module
        updated = queryset.update(order_status='shipped', shipped_at=timezone.now()) #Updates the order status to shipped
        self.message_user(request, f'{updated} orders marked as shipped.') #Displays the message
    mark_as_shipped.short_description = "Mark selected orders as shipped" #Sets the short description for the mark as shipped action

    def mark_as_delivered(self, request, queryset):
        """Mark selected orders as delivered"""
        from django.utils import timezone #Imports the timezone module
        updated = queryset.update(order_status='delivered', delivered_at=timezone.now()) #Updates the order status to delivered
        self.message_user(request, f'{updated} orders marked as delivered.') #Displays the message
    mark_as_delivered.short_description = "Mark selected orders as delivered" #Sets the short description for the mark as delivered action

    def mark_as_cancelled(self, request, queryset):
        """Mark selected orders as cancelled"""
        updated = queryset.update(order_status='cancelled') #Updates the order status to cancelled
        self.message_user(request, f'{updated} orders marked as cancelled.') #Displays the message
    mark_as_cancelled.short_description = "Mark selected orders as cancelled" #Sets the short description for the mark as cancelled action

    def mark_as_paid(self, request, queryset):
        """Mark selected orders as paid"""
        updated = queryset.update(payment_status='paid') #Updates the payment status to paid
        self.message_user(request, f'{updated} orders marked as paid.') #Displays the message
    mark_as_paid.short_description = "Mark selected orders as paid" #Sets the short description for the mark as paid action


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin interface for order items.
    """
    list_display = ['order', 'product_name', 'quantity', 'unit_price', 'total_price'] #Display the fields in the admin interface
    list_filter = ['order__order_status']
    search_fields = ['order__order_number', 'product_name', 'product_sku']
    readonly_fields = ['product_name', 'product_sku', 'unit_price', 'total_price']


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for order status history.
    """
    list_display = ['order', 'status', 'changed_by', 'changed_at'] #Display the fields in the admin interface
    list_filter = ['status', 'changed_at'] #Filter the fields in the admin interface
    search_fields = ['order__order_number', 'changed_by__username'] #Search the fields in the admin interface
    readonly_fields = ['changed_at'] #Excludes the fields from the admin interface
    ordering = ['-changed_at'] #Order the fields in the admin interface


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    """
    Admin interface for shipping methods.
    """
    list_display = ['name', 'cost', 'estimated_days', 'is_active'] #Display the fields in the admin interface
    list_filter = ['is_active', 'estimated_days'] #Filter the fields in the admin interface
    search_fields = ['name', 'description'] #Search the fields in the admin interface
    ordering = ['name'] #Order the fields in the admin interface


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'requires_card_info'] #Display the fields in the admin interface
    list_filter = ['is_active', 'requires_card_info'] #Filter the fields in the admin interface
    search_fields = ['name', 'description'] #Search the fields in the admin interface
    ordering = ['name'] #Order the fields in the admin interface
