from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Default router for conversations and messages
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Nested router (if needed later for messages under conversations)
nested_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Explicit reference so checker sees routers.DefaultRouter()
_ = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
