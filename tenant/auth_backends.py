from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class Auth0Backend(BaseBackend):
    def authenticate(self, request, token=None):
        user_info = JWTAuthentication().get_validated_token(token)
        user_id = user_info['user_id']
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
