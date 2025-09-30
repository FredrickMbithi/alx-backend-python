from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    """Custom manager to get unread messages only"""
    def get_queryset(self):
        return super().get_queryset().filter(is_read=False)


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    objects = models.Manager()  # default manager
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:20]}"


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name="notifications", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message.content[:20]}"
class MessageHistory(models.Model):
    message = models.ForeignKey("Message", on_delete=models.CASCADE, related_name="history")
    edited_at = models.DateTimeField(auto_now=True)
    old_content = models.TextField()

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"