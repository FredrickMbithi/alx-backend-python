from django.test import TestCase

# Create your tests here.


class SimpleMathTest(TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)
