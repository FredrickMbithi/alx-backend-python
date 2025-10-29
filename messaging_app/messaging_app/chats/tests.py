from django.test import TestCase

class SimpleMathTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)
