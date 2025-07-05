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
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'{product_name} removed from cart!')
    return redirect('orders:cart')


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'total_price': cart_item.cart.total_price if cart_item.cart else 0,
                'total_items': cart_item.cart.total_items if cart_item.cart else 0
            })
        else:
            return redirect('orders:cart')
    return JsonResponse({'success': False})


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    payment_methods = PaymentMethod.objects.filter(is_active=True)
    shipping_methods = ShippingMethod.objects.filter(is_active=True)

    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('orders:cart')

    if request.method == 'POST':
        try:
            selected_payment_method_id = request.POST.get('payment_method')
            selected_shipping_method_id = request.POST.get('shipping_method')
            payment_method = PaymentMethod.objects.get(id=selected_payment_method_id) if selected_payment_method_id else None
            shipping_method = ShippingMethod.objects.get(id=selected_shipping_method_id) if selected_shipping_method_id else None
            shipping_cost = shipping_method.cost if shipping_method else 0
            subtotal = cart.total_price
            tax_amount = subtotal * Decimal('0.08')
            total_with_tax = subtotal + tax_amount
            total_amount = total_with_tax + shipping_cost

            order = Order.objects.create(
                user=request.user,
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_cost=shipping_cost,
                total_amount=total_amount,
                shipping_address=request.POST.get('shipping_address', ''),
                shipping_city=request.POST.get('shipping_city', ''),
                shipping_state=request.POST.get('shipping_state', ''),
                shipping_postal_code=request.POST.get('shipping_postal_code', ''),
                shipping_country=request.POST.get('shipping_country', ''),
                shipping_phone=request.POST.get('shipping_phone', ''),
                customer_notes=request.POST.get('customer_notes', ''),
                payment_method=payment_method.name if payment_method else '',
                # Optionally save card info or transaction id here
            )
            # Optionally, you can save the shipping method name in a new field if you want
            # order.shipping_method = shipping_method.name if shipping_method else ''
            # order.save()

            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.current_price,
                    total_price=cart_item.total_price
                )
                # Decrement product stock
                cart_item.product.stock_quantity = max(0, cart_item.product.stock_quantity - cart_item.quantity)
                cart_item.product.save()

            # Create initial status history
            OrderStatusHistory.objects.create(
                order=order,
                status='pending',
                notes='Order placed successfully',
                changed_by=request.user
            )

            # Clear cart
            cart.items.all().delete()

            messages.success(request, f'Order {order.order_number} placed successfully!')
            return redirect('orders:order_detail', order_number=order.order_number)

        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
            return redirect('orders:cart')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'payment_methods': payment_methods,
        'shipping_methods': shipping_methods,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Get status history for this order
    status_history = order.status_history.all()
    
    context = {
        'order': order,
        'status_history': status_history,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_history(request):
    orders = request.user.orders.all()
    
    # Sample orders for demonstration if user has no orders
    if not orders.exists():
        # This is just for demonstration
        pass
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)


@login_required
def cancel_order(request, order_number):
    """Cancel an order if it's still cancellable"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if not order.can_cancel:
        messages.error(request, 'This order cannot be cancelled.')
        return redirect('orders:order_detail', order_number=order_number)
    
    if request.method == 'POST':
        try:
            # Update order status
            order.order_status = 'cancelled'
            order.save()
            
            # Create status history entry
            OrderStatusHistory.objects.create(
                order=order,
                status='cancelled',
                notes=f'Order cancelled by customer: {request.POST.get("cancellation_reason", "No reason provided")}',
                changed_by=request.user
            )
            
            messages.success(request, f'Order {order.order_number} has been cancelled successfully.')
            return redirect('orders:order_history')
            
        except Exception as e:
            messages.error(request, f'Error cancelling order: {str(e)}')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/cancel_order.html', context)


@login_required
def download_invoice(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})


@login_required
def track_order(request, order_number):
    """AJAX endpoint for real-time order tracking"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'order_number': order.order_number,
            'status': order.order_status,
            'status_display': order.get_order_status_display(),
            'payment_status': order.payment_status,
            'payment_status_display': order.get_payment_status_display(),
            'created_at': order.created_at.isoformat(),
            'shipped_at': order.shipped_at.isoformat() if order.shipped_at else None,
            'delivered_at': order.delivered_at.isoformat() if order.delivered_at else None,
            'can_cancel': order.can_cancel,
        })
    
    return redirect('orders:order_detail', order_number=order_number)
