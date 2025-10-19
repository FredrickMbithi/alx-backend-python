# messaging_app/chats/auth.py
"""
Authentication helpers for chats app.

Provides a small utility to generate tokens for a user (used in tests or manual runs).
"""
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Return JWT (refresh + access) for the given user.
    Useful for testing and seeding automated requests.
    """
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
