# messaging/managers.py
from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # Return unread messages where user is the receiver (or sender/recipient logic)
        return self.filter(read=False, sender=user)  # adjust field if you have a receiver
