from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Vendor Dashboard URLs
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor-dashboard/product/create/', views.vendor_product_create, name='vendor_product_create'),
    path('vendor-dashboard/product/<int:product_id>/edit/', views.vendor_product_edit, name='vendor_product_edit'),
    path('vendor-dashboard/product/<int:product_id>/delete/', views.vendor_product_delete, name='vendor_product_delete'),
] 