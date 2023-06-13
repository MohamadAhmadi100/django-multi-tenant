import base64

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from jose import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


from main.config import setting
from .models import Tenant


class Auth0JSONWebTokenAuthentication(BaseAuthentication):

    def __init__(self):
        ...

    def decode_padding(self, base64_string):
        padding = '=' * (4 - (len(base64_string) % 4))
        return base64.urlsafe_b64decode(base64_string + padding)

    def get_jwks(self, auth0_domain):
        url = f'https://{auth0_domain}/.well-known/jwks.json'
        return requests.get(url).json()

    def get_public_key(self, auth0_domain, kid):
        jwks = self.get_jwks(auth0_domain)
        print(jwks)
        for jwk_data in jwks['keys']:
            if jwk_data['kid'] == kid:
                e = int.from_bytes(self.decode_padding(jwk_data['e']), 'big')
                n = int.from_bytes(self.decode_padding(jwk_data['n']), 'big')
                return RSAPublicNumbers(e, n).public_key(default_backend())
        raise Exception('Public key not found')

    def decode_token(self, token, auth0_domain, api_identifier):
        header = jwt.get_unverified_header(token)
        public_key = self.get_public_key(auth0_domain, header['kid'])

        return jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=api_identifier
        )

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        try:
            parts = auth_header.split()
            if parts[0].lower() != 'bearer':
                return None
            if len(parts) == 1:
                raise AuthenticationFailed('No credentials provided.')
            elif len(parts) > 2:
                raise AuthenticationFailed('Token string should not contain spaces.')
            token = parts[1]
            payload = self.decode_token(token, setting.AUTH0_DOMAIN, setting.AUTH0_API_IDENTIFIER)
            print(payload)
        except Tenant.DoesNotExist:
            request.tenant = None
        return "response"
# tenant_id = payload.get("https://your-namespace/tenant_id")
#         tenant = Tenant.objects.get(auth0_tenant_id=tenant_id)
#         return (tenant, None)
#
#     except (Tenant.DoesNotExist, jose.jwt.JWTError):
#     raise AuthenticationFailed('No tenant found or Invalid token')
