# chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction

from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .pagination import MessagePagination
from .filters import MessageFilter

# Get the user model
User = get_user_model()


# ------------------------
# User ViewSet
# ------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and manage users.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


# ------------------------
# Conversation ViewSet
# ------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and manage conversations.
    Only returns conversations where the logged-in user is a participant.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants')


# ------------------------
# Message ViewSet
# ------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and manage messages.
    Only returns messages from conversations the user is a participant in.
    Supports filtering and pagination.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = MessagePagination

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        if not conversation_id:
            return Response(
                {"error": "conversation_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Force sender = logged-in user
        data = request.data.copy()
        data['sender'] = request.user.id  # integer instead of string
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(
            self.get_serializer(message).data,
            status=status.HTTP_201_CREATED
        )
