from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(decimal_places=2, max_digits=10)
    shipping_charge = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"

class OrderDetails(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField()

    class Meta:
        db_table = "order_details"