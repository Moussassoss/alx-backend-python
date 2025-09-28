from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import exceptions

def get_tokens_for_user(user):
    """
    Generate refresh and access tokens for a user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def authenticate_user(email, password):
    """
    Authenticate a user using email and password.
    Returns the user instance if credentials are valid.
    """
    user = authenticate(username=email, password=password)
    if user is None:
        raise exceptions.AuthenticationFailed('Invalid email or password')
    return user
