
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# /users
urlpatterns = [
    path('/login', TokenObtainPairView.as_view(), name='token'),
    path('/login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
