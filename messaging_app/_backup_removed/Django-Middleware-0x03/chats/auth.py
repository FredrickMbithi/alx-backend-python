from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication.
    You can extend this later with extra checks.
    """
    def authenticate(self, request):
        return super().authenticate(request)
