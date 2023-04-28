from food_app_users.views import *
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/',RegisterAPI.as_view(),name='register'),
    path('login/',LoginAPIView.as_view(),name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]