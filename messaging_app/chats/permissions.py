from rest_framework import permissions

class IsOwner(BasePermissions):
    """
    Custom permission class (not actively used in views).
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "sender"):
            return obj.sender == request.user
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        return False


from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Allow only participants of a conversation to view, send, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        # Case 1: If object is a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Case 2: If object is a Message
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
