from django.urls import path

from .views import ProductList, ProductDetail, ReviewList, ReviewDetails

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:product_id>/', ProductDetail.as_view()),
    path('product_reviews/', ReviewList.as_view()),
    path('product_reviews/<str:review_id>/', ReviewDetails.as_view())
]