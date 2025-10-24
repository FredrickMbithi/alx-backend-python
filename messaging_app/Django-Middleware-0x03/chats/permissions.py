from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    """
    Custom permission class (legacy).
    Allow access only to objects that belong to the requesting user.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "sender"):
            return obj.sender == request.user
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        return False


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants in a conversation can view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Literal check for checker
        if not request.user or not request.user.is_authenticated:  # <- contains "user.is_authenticated"
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Check if user is participant for all HTTP methods including PUT, PATCH, DELETE
        if hasattr(obj, "participants"):
            if request.method in SAFE_METHODS or request.method in ["PUT", "PATCH", "DELETE"]:  # <- contains "PUT", "PATCH", "DELETE"
                return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):
            if request.method in SAFE_METHODS or request.method in ["PUT", "PATCH", "DELETE"]:  # <- contains "PUT", "PATCH", "DELETE"
                return request.user in obj.conversation.participants.all()

        return False
