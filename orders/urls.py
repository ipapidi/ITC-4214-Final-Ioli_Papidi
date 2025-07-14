from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<str:order_number>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<str:order_number>/invoice/', views.download_invoice, name='download_invoice'),
    path('order/<str:order_number>/track/', views.track_order, name='track_order'),
] 