from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

# ... previous signals ...

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Creates a Notification whenever a new Message is saved.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,  # make sure your Notification model has a 'user' field
            message=instance          # and a 'message' ForeignKey field
        )
        print(f"Notification created for message {instance.id} to {instance.receiver}")
