# chats/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create DRF router using routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include the router URLs in urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
