from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name',
                  'email', 'phone_number', 'role', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    sender = UserSerializer(read_only=True)
    message_preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'conversation',
                  'message_body', 'sent_at', 'message_preview']

    def get_message_preview(self, obj):
        """Return first 20 chars of message body"""
        return obj.message_body[:20]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model with nested messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def validate(self, data):
        """
        Ensure a conversation has at least one participant.
        """
        if not data.get("participants"):
            raise serializers.ValidationError("Conversation must have participants")
        return data
