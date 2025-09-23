# chats/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    # Add filtering support
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if not participants_ids or len(participants_ids) < 2:
            return Response(
                {"error": "A conversation must have at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(user_id__in=participants_ids))
        conversation.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.select_related('sender', 'conversation').all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # Add filtering support
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['sender'] = str(request.user.user_id)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
