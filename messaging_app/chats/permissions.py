from rest_framework.permissions import BasePermission

class IsParticipantOfConversation(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is a Conversation
        return request.user in obj.participants.all()
