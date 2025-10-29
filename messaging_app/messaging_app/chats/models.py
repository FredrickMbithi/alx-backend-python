# chats/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

# Use the project's configured user model to stay consistent with AUTH_USER_MODEL
User = get_user_model()


class Conversation(models.Model):
    """
    Represents a conversation between multiple users
    """
    # Refer to the user model using the AUTH_USER_MODEL string to avoid import issues
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        # Use the actual user instances for display
        names = [u.username for u in self.participants.all()[:3]]
        participant_names = ', '.join(names)
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
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        sender_username = getattr(self.sender, 'username', str(self.sender))
        preview = (self.message_body[:50] + '...') if len(self.message_body) > 50 else self.message_body
        return f"{sender_username}: {preview}"
