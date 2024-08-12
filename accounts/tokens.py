from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Extend the Django PasswordResetTokenGenerator to create a token generator for account activation
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    # Override the method to generate a hash value that will be used in creating a token
    def _make_hash_value(self, user, timestamp):
        # The hash value is a combination of the user's primary key (pk), the timestamp,
        # and the user's is_active status. This ensures the token is unique and secure.
        # Changing the user's is_active status invalidates the token.
        return str(user.pk) + str(timestamp) + str(user.is_active)

# Create an instance of the token generator class
account_activation_token = AccountActivationTokenGenerator()
