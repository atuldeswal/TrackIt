from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Extend the AbstractUser model to customize the user model for the application.
class user_accounts(AbstractUser):
    # Set username to None because we are using email as the primary identifier for authentication.
    username = None
    # Define an email field that must be unique across all instances, to be used for authentication.
    email = models.EmailField(unique=True)
    # Add an is_verified field to track whether a user's email has been verified.
    is_verified = models.BooleanField(default=False)

    # Set the USERNAME_FIELD to 'email' to use it for authentication instead of the default 'username'.
    USERNAME_FIELD = 'email'
    # Since we are not adding any additional required fields, leave REQUIRED_FIELDS empty.
    REQUIRED_FIELDS = []

    # Specify a custom manager for the user_accounts model.
    objects = UserManager()
