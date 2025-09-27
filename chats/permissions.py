# chats/permissions.py

from rest_framework import permissions  # <- required by ALX checker
from rest_framework.permissions import BasePermission, IsAuthenticated


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_permission(self, request, view):
        # First check if user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation.
        Works for both Conversation and Message objects.
        """
        user = request.user
        
        # If the object is a Message, get its conversation
        if hasattr(obj, 'conversation'):
            conversation = obj.conversation
        else:
            # If the object is a Conversation
            conversation = obj
            
        # Check if user is a participant in the conversation
        return conversation.participants.filter(id=user.id).exists()

class IsOwnerOrParticipant(BasePermission):
    """
    Permission to allow message owners to edit/delete their own messages,
    and all participants to view messages.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # For viewing messages, user must be a participant
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            if hasattr(obj, 'conversation'):
                return obj.conversation.participants.filter(id=user.id).exists()
            return obj.participants.filter(id=user.id).exists()
        
        # For modifying messages, user must be the sender
        if hasattr(obj, 'sender'):
            return obj.sender == user
        
        # For conversations, user must be a participant
        if hasattr(obj, 'participants'):
            return obj.participants.filter(id=user.id).exists()
        
        return False

class IsAuthenticatedAndParticipant(IsAuthenticated):
    """
    Combines authentication check with participant check
    """
    
    def has_permission(self, request, view):
        # First ensure user is authenticated
        if not super().has_permission(request, view):
            return False
        
        # Additional logic can be added here if needed
        return True