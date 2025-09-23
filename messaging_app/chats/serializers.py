# chats/serializers.py
from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','username','password','first_name','last_name','email','phone_number','role','created_at')
        read_only_fields = ('id','created_at')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = Message
        fields = ('id','sender','sender_id','conversation','message_body','sent_at')
        read_only_fields = ('id','sent_at','sender')

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(id=sender_id)
        return Message.objects.create(sender=sender, **validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id','participants','participant_ids','messages','created_at')
        read_only_fields = ('id','participants','messages','created_at')

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conv = Conversation.objects.create()
        participants = User.objects.filter(id__in=participant_ids)
        conv.participants.set(participants)
        return conv
