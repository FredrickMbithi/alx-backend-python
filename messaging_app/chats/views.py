from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsParticipantOfConversation
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def get_queryset(self):
        # Only return conversations where the logged-in user is a participant
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    def get_queryset(self):
        # Only return messages from conversations the user is a participant in
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # ✅ Require conversation_id
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

        # ✅ Check if user is participant, else return 403
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Force sender = logged-in user
        data = request.data.copy()
        data['sender'] = str(request.user.user_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
