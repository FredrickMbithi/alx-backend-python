from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allow access only to objects that belong to the requesting user.
    """

    def has_object_permission(self, request, view, obj):
        # For Messages
        if hasattr(obj, "sender"):
            return obj.sender == request.user
        # For Conversations (user must be a participant)
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        return False
