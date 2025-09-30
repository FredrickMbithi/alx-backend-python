from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    Deletes all user-related data when a user is deleted.
    """
    # Optional if CASCADE already handles this:
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, no history to log
        return
    
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        # Message content changed
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content,
            edited_by=instance.edited_by  # must be set when updating the message
        )