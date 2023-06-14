import base64
import logging

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from jose import jwt
from main.config import setting
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MainUser:
    def __init__(self, organization_id, user_id):
        self.organization_id = organization_id
        self.user_id = user_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_staff(self):
        return False


class Auth0JSONWebTokenAuthentication(BaseAuthentication):

    def __init__(self):
        ...

    def decode_padding(self, base64_string):
        padding = '=' * (4 - (len(base64_string) % 4))
        return base64.urlsafe_b64decode(base64_string + padding)

    @staticmethod
    def get_jwks():
        return requests.get(setting.AUTH0_JWKS_URL).json()

    def get_public_key(self, kid):
        jwks = self.get_jwks()
        for jwk_data in jwks['keys']:
            if jwk_data['kid'] == kid:
                e = int.from_bytes(self.decode_padding(jwk_data['e']), 'big')
                n = int.from_bytes(self.decode_padding(jwk_data['n']), 'big')
                return RSAPublicNumbers(e, n).public_key(default_backend())
        raise AuthenticationFailed("Invalid token")

    def decode_token(self, token, audience):
        header = jwt.get_unverified_header(token)
        public_key = self.get_public_key(header['kid'])

        return jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=audience
        )

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authorization header not provided')

        parts = auth_header.split()
        if parts[0].lower() != 'bearer':
            raise AuthenticationFailed('Invalid token header')
        if len(parts) == 1:
            raise AuthenticationFailed('No credentials provided')
        if len(parts) > 2:
            raise AuthenticationFailed('Token string should not contain spaces')

        token = parts[1]
        try:
            payload = self.decode_token(token, setting.AUTH0_AUDIENCE)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.JWTClaimsError:
            raise AuthenticationFailed('Incorrect claims, please check the audience and issuer')
        except Exception as ex:
            logging.error(ex, exc_info=True)
            raise AuthenticationFailed('Could not decode token')
        subject_claim = payload.get('sub')
        request.organization_id = payload.get("org_id")
        request.user_id = subject_claim.split('|')[1]
        user = MainUser(organization_id=request.organization_id, user_id=request.user_id)
        return user, None
# tenant_id = payload.get("https://your-namespace/tenant_id")
#         tenant = Tenant.objects.get(auth0_tenant_id=tenant_id)
#         return (tenant, None)
#
#     except (Tenant.DoesNotExist, jose.jwt.JWTError):
#     raise AuthenticationFailed('No tenant found or Invalid token')
