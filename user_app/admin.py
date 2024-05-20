from django.contrib import admin
from .models import User, OrderModel


# Register your models here.
admin.site.register(User)
admin.site.register(OrderModel)