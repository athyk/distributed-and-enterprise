from django.test import TestCase
from models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        """Test if a user can be created successfully"""
        user = User.objects.create(
            email="test@example.com",
            password="securepassword",
            full_name="Test User",
            first_name="Test",
            last_name="User"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.full_name, "Test User")
        self.assertFalse(user.email_verified)  # Default value check