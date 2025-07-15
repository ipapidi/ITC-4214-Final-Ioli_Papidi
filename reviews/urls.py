from django.urls import path
from . import views

app_name = 'reviews' #Set the app name

urlpatterns = [ #Set the url patterns
    path('product/<int:product_id>/reviews/', views.product_reviews, name='product_reviews'), #Set the product reviews
    path('product/<int:product_id>/review/add/', views.add_review, name='add_review'), #Set the add review
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'), #Set the edit review
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'), #Set the delete review
] 