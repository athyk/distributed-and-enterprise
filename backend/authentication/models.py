from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator

class User(models.Model):
    email = models.TextField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                message="Enter a valid email address.",
                code="invalid_email",
            )
        ],
    )
    email_verified = models.BooleanField(default=False)
    password = models.TextField()
    two_fa_secret = models.TextField(blank=True, null=True)
    
    full_name = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    nickname = models.CharField(max_length=50, blank=True, null=True)
    
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
        ("Prefer not to say", "Prefer not to say"),
    ]
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    picture_url = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"  # Match PostgreSQL table name
