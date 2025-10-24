from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def home(request):
    return HttpResponse("Hello, Middleware project is running ✅")

urlpatterns = [
    path("", home),  # 👈 root URL route
    path("admin/", admin.site.urls),
    path("api/", include("chats.urls")),
    path("api-auth/", include("rest_framework.urls")),  # browsable login
    # JWT auth endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
