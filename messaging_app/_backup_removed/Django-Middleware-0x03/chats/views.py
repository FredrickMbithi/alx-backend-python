# chats/views.py

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Example logic
        return request.user in obj.participants.all() or obj.owner == request.user


from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    ConversationDetailSerializer, 
    MessageSerializer, 
    UserSerializer
)
from .permissions import IsParticipantOfConversation, IsOwnerOrParticipant
from .filters import ConversationFilter, MessageFilter
from .pagination import ConversationPagination, MessagePagination

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__username', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-updated_at']
    pagination_class = ConversationPagination
    
    def get_queryset(self):
        """
        Return only conversations where the current user is a participant
        """
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages').distinct()
    
    def get_serializer_class(self):
        """
        Use detailed serializer for retrieve action
        """
        if self.action == 'retrieve':
            return ConversationDetailSerializer
        return ConversationSerializer
    
    def perform_create(self, serializer):
        """
        Ensure the current user is added as a participant when creating a conversation
        """
        serializer.save()
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific conversation
        """
        conversation = self.get_object()
        messages = conversation.messages.all()
        
        # Apply filtering
        filter_backend = DjangoFilterBackend()
        filtered_messages = filter_backend.filter_queryset(request, messages, MessageViewSet)
        
        # Apply pagination
        paginator = MessagePagination()
        page = paginator.paginate_queryset(filtered_messages, request)
        
        if page is not None:
            serializer = MessageSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(filtered_messages, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Add a user to the conversation
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({'message': f'User {user.username} added to conversation'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        """
        Remove a user from the conversation
        """
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.remove(user)
            return Response({'message': f'User {user.username} removed from conversation'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParticipant]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['timestamp']
    ordering = ['timestamp']
    pagination_class = MessagePagination
    
    def get_queryset(self):
        """
        Return only messages from conversations where the current user is a participant
        """
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation').distinct()
    
    def perform_create(self, serializer):
        """
        Set the sender to the current user when creating a message
        """
        serializer.save(sender=self.request.user)
    
    def perform_update(self, serializer):
        """
        Only allow users to update their own messages
        """
        if serializer.instance.sender != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own messages")
        serializer.save()
    
    def perform_destroy(self, instance):
        """
        Only allow users to delete their own messages
        """
        if instance.sender != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own messages")
        instance.delete()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing users (for finding conversation participants)
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    def get_queryset(self):
        """
        Return all users except the current user
        """
        return User.objects.exclude(id=self.request.user.id)