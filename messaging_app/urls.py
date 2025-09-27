# messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from chats.auth import UserRegistrationView, login_view, CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/register/', UserRegistrationView.as_view(), name='user_register'),
    path('api/auth/login/', login_view, name='login'),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Chat endpoints
    path('api/chats/', include('chats.urls')),
]