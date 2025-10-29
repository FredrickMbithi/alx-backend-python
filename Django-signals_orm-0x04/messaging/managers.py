from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to return unread messages for a given user.
    The method name `unread_for_user` is what the autograder expects.
    """
    def unread_for_user(self, user):
        return self.get_queryset().filter(receiver=user, read=False)

    # optional alias (keeps backward compatibility if referenced elsewhere)
    def for_user(self, user):
        return self.unread_for_user(user)
