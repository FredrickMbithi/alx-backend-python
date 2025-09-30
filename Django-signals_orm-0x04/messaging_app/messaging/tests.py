from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='pass123')
        self.receiver = User.objects.create_user(username='receiver', password='pass123')
    
    def test_notification_created_on_message_save(self):
        """Test that a notification is created when a message is saved"""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message"
        )
        
        # Check if notification was created
        notification = Notification.objects.filter(user=self.receiver, message=message)
        self.assertTrue(notification.exists())
        self.assertEqual(notification.count(), 1)