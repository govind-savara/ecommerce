from django.contrib.auth import views as auth_views
from django.urls import path

from .auth_views import user_login, user_logout, user_signup, loggedin_user
from .views import place_order

urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user/', loggedin_user, name='user'),
    path('place_order/', place_order, name='place_order'),
]
