from django.urls import path

from .views import get_product_popularity_details

urlpatterns = [
    path("get_product_popularity_details/", get_product_popularity_details)
]
