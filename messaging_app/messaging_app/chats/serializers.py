# chats/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    class Meta:
        model = User
        # Some user models may use 'id' or 'user_id' as the primary key.
        # Keep commonly used display fields; adjust if you have a custom user model.
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_id', 'message_body', 'timestamp']
        read_only_fields = ['id', 'timestamp']
    
    def create(self, validated_data):
        # Set sender to current user if not provided
        if 'sender_id' not in validated_data:
            validated_data['sender'] = self.context['request'].user
        else:
            validated_data['sender_id'] = validated_data.pop('sender_id')
        return super().create(validated_data)

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    last_message = MessageSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participant_ids', 'created_at', 'updated_at', 
                 'last_message', 'message_count']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        """Get the total number of messages in this conversation"""
        return obj.messages.count()
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = super().create(validated_data)
        
        # Add the current user as a participant
        conversation.participants.add(self.context['request'].user)
        
        # Add other participants
        if participant_ids:
            # Try filtering by 'id' first, fall back to 'user_id' for custom PKs
            try:
                users = User.objects.filter(id__in=participant_ids)
            except Exception:
                users = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.add(*users)
        
        return conversation

class ConversationDetailSerializer(ConversationSerializer):
    """
    Detailed serializer for Conversation with recent messages
    """
    messages = MessageSerializer(many=True, read_only=True)
    recent_messages = serializers.SerializerMethodField()
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages', 'recent_messages']
    
    def get_recent_messages(self, obj):
        """Get the last 10 messages from this conversation"""
        recent_messages = obj.messages.all()[:10]
        return MessageSerializer(recent_messages, many=True, context=self.context).data