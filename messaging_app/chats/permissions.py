from rest_framework import permissions

class IsOwner(permissions):
    """
    Custom permission class (not actively used in views).
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "sender"):
            return obj.sender == request.user
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()
        return False
