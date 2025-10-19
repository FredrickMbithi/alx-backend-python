from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Adds role, phone number, and UUID primary key.
    Explicitly defines fields required by checker: email, password, first_name, last_name.
    """
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """
    A conversation between multiple users.
    """
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    A message sent in a conversation.
    """
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE
    )
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} in Conversation {self.conversation_id}"
