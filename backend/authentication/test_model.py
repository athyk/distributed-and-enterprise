from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from models import User

class UserModelTest(TestCase):
    def setUp(self):
        """Set up a test user."""
        self.user = User.objects.create(
            email="test@example.com",
            password="securepassword",
            full_name="Test User",
            first_name="Test",
            last_name="User"
        )

    def test_user_creation(self):
        """Test if a user is created successfully."""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertFalse(self.user.email_verified)  # Default value
        self.assertIsNone(self.user.two_fa_secret)  # Default None

    def test_unique_email(self):
        """Test that emails must be unique."""
        with self.assertRaises(IntegrityError):
            User.objects.create(email="test@example.com", password="anotherpassword")

    def test_invalid_email(self):
        """Test that an invalid email raises a ValidationError."""
        user = User(email="invalid-email", password="password")
        with self.assertRaises(ValidationError):
            user.full_clean()  # Triggers validation

    def test_nickname_length(self):
        """Test that nickname cannot exceed max length."""
        long_nickname = "a" * 51  # Exceeds max_length=50
        user = User(email="new@example.com", password="password", nickname=long_nickname)
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_gender_choices(self):
        """Test that gender choices are enforced."""
        user = User(email="valid@example.com", password="password", gender="InvalidChoice")
        with self.assertRaises(ValidationError):
            user.full_clean()
