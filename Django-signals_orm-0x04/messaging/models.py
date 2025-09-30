# messaging/models.py
from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager  # <-- import it here

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )
    edited_by = models.ForeignKey(User, null=True, blank=True, related_name='edited_messages', on_delete=models.SET_NULL)
    
    read = models.BooleanField(default=False)  # track read/unread

    # Managers
    objects = models.Manager()         # default manager
    unread = UnreadMessagesManager()   # <-- attach your custom manager here
