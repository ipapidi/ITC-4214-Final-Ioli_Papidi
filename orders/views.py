from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory, ShippingMethod, PaymentMethod
from products.models import Product
from decimal import Decimal


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user) #Gets or creates the cart for the user
    cart_items = cart.items.all() #Gets all the items in the cart

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/cart.html', context) #Renders the cart template


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id) #Gets the product
    cart, created = Cart.objects.get_or_create(user=request.user) #Gets or creates the cart for the user

    cart_item, created = CartItem.objects.get_or_create( #Gets or creates the cart item
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1 #Increments the quantity
        cart_item.save() #Saves the cart item

    messages.success(request, f'{product.name} added to cart!') #Displays the message
    return redirect('orders:cart') #Redirects to the cart view


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user) #Gets the cart item
    product_name = cart_item.product.name #Gets the product name
    cart_item.delete() #Deletes the cart item

    messages.success(request, f'{product_name} removed from cart!') #Displays the message
    return redirect('orders:cart') #Redirects to the cart view


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user) #Gets the cart item
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1)) #Gets the quantity
        if quantity > 0:
            cart_item.quantity = quantity #Sets the quantity
            cart_item.save() #Saves the cart item
        else:
            cart_item.delete() #Deletes the cart item
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True, #Sets the success to true
                'total_price': cart_item.cart.total_price if cart_item.cart else 0, #Gets the total price
                'total_items': cart_item.cart.total_items if cart_item.cart else 0 #Gets the total items
            })
        else:
            return redirect('orders:cart') #Redirects to the cart view
    return JsonResponse({'success': False}) #Returns the JSON response


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user) #Gets or creates the cart for the user
    cart_items = cart.items.all() #Gets all the items in the cart
    payment_methods = PaymentMethod.objects.filter(is_active=True) #Gets all the active payment methods
    shipping_methods = ShippingMethod.objects.filter(is_active=True)

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!') #Displays the message
        return redirect('orders:cart') #Redirects to the cart view

    if request.method == 'POST':
        try:
            selected_payment_method_id = request.POST.get('payment_method') #Gets the payment method
            selected_shipping_method_id = request.POST.get('shipping_method') #Gets the shipping method
            payment_method = PaymentMethod.objects.get(id=selected_payment_method_id) if selected_payment_method_id else None #Gets the payment method
            shipping_method = ShippingMethod.objects.get(id=selected_shipping_method_id) if selected_shipping_method_id else None #Gets the shipping method
            shipping_cost = shipping_method.cost if shipping_method else 0 #Gets the shipping cost
            subtotal = cart.total_price #Gets the subtotal
            tax_amount = subtotal * Decimal('0.24')  # 24% tax rate to match Cart model
            total_with_tax = subtotal + tax_amount #Gets the total with tax
            total_amount = total_with_tax + shipping_cost #Gets the total amount

            order = Order.objects.create( #Creates the order
                user=request.user,
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_cost=shipping_cost,
                total_amount=total_amount,
                shipping_address=request.POST.get('shipping_address', ''), #Gets the shipping address
                shipping_city=request.POST.get('shipping_city', ''), #Gets the shipping city
                shipping_state=request.POST.get('shipping_state', ''), #Gets the shipping state
                shipping_postal_code=request.POST.get('shipping_postal_code', ''),
                shipping_country=request.POST.get('shipping_country', ''),
                shipping_phone=request.POST.get('shipping_phone', ''),
                customer_notes=request.POST.get('customer_notes', ''),
                payment_method=payment_method.name if payment_method else '', #Gets the payment method
            )

            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order, #Sets the order
                    product=cart_item.product, #Sets the product
                    quantity=cart_item.quantity, #Sets the quantity
                    unit_price=cart_item.product.current_price, #Sets the unit price
                    total_price=cart_item.total_price #Sets the total price
                )
                # Decrement product stock
                cart_item.product.stock_quantity = max(0, cart_item.product.stock_quantity - cart_item.quantity) 
                cart_item.product.save()

            # Create initial status history
            OrderStatusHistory.objects.create(
                order=order, #Sets the order
                status='pending', #Sets the status
                notes='Order placed successfully', #Sets the notes
                changed_by=request.user #Sets the changed by
            )

            # Clear cart
            cart.items.all().delete() #Deletes all the items in the cart

            messages.success(request, f'Order {order.order_number} placed successfully!') #Displays the message
            return redirect('orders:order_detail', order_number=order.order_number) #Redirects to the order detail view

        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}') #Displays the message
            return redirect('orders:cart') #Redirects to the cart view

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'payment_methods': payment_methods,
        'shipping_methods': shipping_methods,
    }
    return render(request, 'orders/checkout.html', context) #Renders the checkout template


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user) #Gets the order

    # Get status history for this order
    status_history = order.status_history.all() #Gets the status history

    context = {
        'order': order,
        'status_history': status_history,
    }
    return render(request, 'orders/order_detail.html', context) #Renders the order detail template


@login_required
def order_history(request):
    orders = request.user.orders.all() #Gets all the orders for the user

    # Sample orders for demonstration if user has no orders
    if not orders.exists():
        # This is just for demonstration
        pass

    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context) #Renders the order history template


@login_required
def cancel_order(request, order_number):
    """Cancel an order if it's still cancellable"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user) #Gets the order

    if not order.can_cancel:
        messages.error(request, 'This order cannot be cancelled.') #Displays the message
        return redirect('orders:order_detail', order_number=order_number) #Redirects to the order detail view

    if request.method == 'POST':
        try:
            # Update order status
            order.order_status = 'cancelled' #Sets the order status to cancelled
            order.save() #Saves the order

            # Create status history entry
            OrderStatusHistory.objects.create(
                order=order, #Sets the order
                status='cancelled', #Sets the status
                notes=f'Order cancelled by customer: {request.POST.get("cancellation_reason", "No reason provided")}', #Sets the notes
                changed_by=request.user #Sets the changed by
            )

            messages.success(request, f'Order {order.order_number} has been cancelled successfully.') #Displays the message
            return redirect('orders:order_history') #Redirects to the order history view

        except Exception as e:
            messages.error(request, f'Error cancelling order: {str(e)}') #Displays the message

    context = {
        'order': order,
    }
    return render(request, 'orders/cancel_order.html', context) #Renders the cancel order template


@login_required
def download_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user) #Gets the order
    return render(request, 'orders/invoice.html', {'order': order}) #Renders the invoice template


@login_required
def track_order(request, order_number):
    """AJAX endpoint for real-time order tracking"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user) #Gets the order

    if request.headers.get('x-requested-with') == 'XMLHttpRequest': #Checks if the request is an AJAX request
        return JsonResponse({
            'order_number': order.order_number, #Gets the order number
            'status': order.order_status, #Gets the order status
            'status_display': order.get_order_status_display(), #Gets the order status display
            'payment_status': order.payment_status, #Gets the payment status
            'payment_status_display': order.get_payment_status_display(), #Gets the payment status display
            'created_at': order.created_at.isoformat(), #Gets the created at
            'shipped_at': order.shipped_at.isoformat() if order.shipped_at else None, #Gets the shipped at
            'delivered_at': order.delivered_at.isoformat() if order.delivered_at else None, #Gets the delivered at
            'can_cancel': order.can_cancel, #Gets the can cancel
        }) #Returns the JSON response

    return redirect('orders:order_detail', order_number=order_number) #Redirects to the order detail view
