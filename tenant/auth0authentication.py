import base64
import logging

import requests
import sentry_sdk
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from django.core.cache import cache
from jose import jwt
from main.config import setting
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .management.commands.create_database import OrganizationDatabaseManager
from .models import MainUser, Organization


class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def __init__(self):
        ...

    @staticmethod
    def decode_padding(base64_string):
        """
        Decode base64 string with padding
        """
        padding = '=' * (4 - (len(base64_string) % 4))
        return base64.urlsafe_b64decode(base64_string + padding)

    @staticmethod
    def get_jwks():
        """
        Retrieve JWKS from Auth0
        """
        jwks = cache.get("jwks")
        if not jwks:
            jwks = requests.get(setting.AUTH0_JWKS_URL).json()
            cache.set("jwks", jwks, 86400)
        return jwks

    def get_public_key(self, kid):
        """
        Get public key from JWKS using the provided key ID (kid)
        """
        jwks = self.get_jwks()
        for jwk_data in jwks['keys']:
            if jwk_data['kid'] == kid:
                e = int.from_bytes(self.decode_padding(jwk_data['e']), 'big')
                n = int.from_bytes(self.decode_padding(jwk_data['n']), 'big')
                return RSAPublicNumbers(e, n).public_key(default_backend())
        raise AuthenticationFailed("Public key for token could not be found.")

    def decode_token(self, token):
        """
        Decode and validate the token
        """
        try:
            header = jwt.get_unverified_header(token)
        except Exception as ex:
            logging.error(ex, exc_info=True)
            sentry_sdk.capture_exception(ex)
            raise AuthenticationFailed('Error parsing token header.')

        try:
            public_key = self.get_public_key(header['kid'])
            return jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=setting.AUTH0_AUDIENCE
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.JWTClaimsError:
            raise AuthenticationFailed('Incorrect claims, please check the audience and issuer.')
        except Exception as ex:
            sentry_sdk.capture_exception(ex)
            logging.error(ex, exc_info=True)
            raise AuthenticationFailed('Error decoding token.')

    def get_token_from_header(self, auth_header):
        """
        Extract token from Authorization header
        """
        if not auth_header:
            raise AuthenticationFailed('Authorization header not provided.')

        parts = auth_header.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            raise AuthenticationFailed('Invalid authorization header format.')

        return parts[1]

    def authenticate(self, request):
        """
        Authenticate the user using Auth0
        """
        # Extract token from Authorization header
        try:
            auth_header = request.headers.get('Authorization')
            token = self.get_token_from_header(auth_header)

            # Decode and validate the token
            payload = self.decode_token(token)

            # Process and store relevant claims
            subject_claim = payload.get('sub')
            organization_id = payload.get("org_id")
            user_id = subject_claim.split('|')[1] if subject_claim else None

            if not organization_id or not user_id:
                raise AuthenticationFailed('Invalid token claims.')

            # Retrieve or create organization and user instances
            organization, organization_created = Organization.objects.get_or_create(organization_id=organization_id)
            if organization_created and organization_id != setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY:
                with OrganizationDatabaseManager() as manager:
                    manager.create_organization_database(organization_id=organization_id)
            request.organization_id = payload.get("org_id")
            request.user_id = subject_claim.split('|')[1]
            user, _user_created = MainUser.objects.get_or_create(user_id=request.user_id, organization=organization)
            return user, organization
        except Exception as ex:
            sentry_sdk.capture_exception(ex)
            logging.error(ex, exc_info=True)
            raise AuthenticationFailed(ex)
