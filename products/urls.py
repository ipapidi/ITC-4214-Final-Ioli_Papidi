from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'), #Sets the home page
    path('products/', views.product_list, name='product_list'), #Product list page
    path('product/<slug:slug>/', views.product_detail, name='product_detail'), #Product detail page
    path('category/<slug:slug>/', views.category_detail, name='category_detail'), #Category detail page
    path('subcategory/<slug:category_slug>/<slug:subcategory_slug>/', views.subcategory_detail, name='subcategory_detail'), #Subcategory detail page
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'), #Brand detail page
    path('search/', views.search, name='search'), #Search page
    path('about/', views.about, name='about'), #About page
    path('contact/', views.contact, name='contact'), #Contact page
    path('recently-viewed/', views.recently_viewed, name='recently_viewed'), #Recently viewed page
    path('ajax/subcategories/', views.get_subcategories, name='get_subcategories'), #Ajax subcategories page
] 