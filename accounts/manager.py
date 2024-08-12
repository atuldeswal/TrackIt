from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    # Create a regular user with an email and password
    def create_user(self, email, password=None, **extra_fields):
        # Validate that an email is provided; if not, raise a ValueError
        if not email:
            raise ValueError("Email is required")

        # Normalize the email address by lowercasing the domain part of it
        email = self.normalize_email(email)
        # Create a new user model instance with the normalized email and extra fields
        user = self.model(email=email, **extra_fields)
        # Set the user's password. This also handles password hashing
        user.set_password(password)
        # Save the user instance to the database
        user.save(using=self._db)

        return user

    # Create a superuser with all permissions, meant for admin and development use
    def create_superuser(self, email, password=None, **extra_fields):
        # Set default parameters for a superuser. A superuser has all permissions.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        # Validate that the is_staff and is_superuser flags are set to True
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Create and return a superuser using the create_user method
        return self.create_user(email, password, **extra_fields)
