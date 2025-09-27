# chats/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Conversation(models.Model):
    """
    Represents a conversation between multiple users
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = ', '.join([user.username for user in self.participants.all()[:3]])
        if self.participants.count() > 3:
            participant_names += '...'
        return f"Conversation: {participant_names}"
    
    @property
    def last_message(self):
        """Get the last message in this conversation"""
        return self.messages.last()

class Message(models.Model):
    """
    Represents a message within a conversation
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.message_body[:50]}{'...' if len(self.message_body) > 50 else ''}"