from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessagingSignalTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="password")
        self.bob = User.objects.create_user(username="bob", password="password")

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.alice, receiver=self.bob, content="Hello Bob!")
        notif = Notification.objects.filter(user=self.bob, message=msg)
        self.assertTrue(notif.exists(), "Notification should be created when a message is sent")
