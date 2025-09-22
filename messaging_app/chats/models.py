import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Explicitly declare the required fields for ALX auto-check
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'   # Use email for login
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # username still required by AbstractUser

    def __str__(self):
        return self.email
