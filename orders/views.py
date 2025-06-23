from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product


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
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'total_price': cart_item.cart.total_price,
            'total_items': cart_item.cart.total_items
        })
    
    return JsonResponse({'success': False})


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty!')
        return redirect('orders:cart')
    
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            subtotal=cart.total_price,
            tax_amount=cart.total_price * 0.08,
            shipping_cost=10.00,
            total_amount=cart.total_price_with_tax + 10.00,
            shipping_address=request.POST.get('shipping_address', ''),
            shipping_city=request.POST.get('shipping_city', ''),
            shipping_state=request.POST.get('shipping_state', ''),
            shipping_postal_code=request.POST.get('shipping_postal_code', ''),
            shipping_country=request.POST.get('shipping_country', ''),
            shipping_phone=request.POST.get('shipping_phone', ''),
        )
        
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.current_price,
                total_price=cart_item.total_price
            )
        
        cart.items.all().delete()
        messages.success(request, f'Order {order.order_number} placed successfully!')
        return redirect('orders:order_detail', order_number=order.order_number)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_history(request):
    orders = request.user.orders.all()
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_history.html', context)
