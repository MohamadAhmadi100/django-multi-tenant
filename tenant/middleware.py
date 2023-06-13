# import base64
#
# import requests
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
# from jose import jwt
#
# from main import config
# from .models import Tenant
#
#
# class TenantMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def decode_padding(self, base64_string):
#         padding = '=' * (4 - (len(base64_string) % 4))
#         return base64.urlsafe_b64decode(base64_string + padding)
#
#     def get_jwks(self, auth0_domain):
#         url = f'https://{auth0_domain}/.well-known/jwks.json'
#         return requests.get(url).json()
#
#     def get_public_key(self, auth0_domain, kid):
#         jwks = self.get_jwks(auth0_domain)
#         for jwk_data in jwks['keys']:
#             if jwk_data['kid'] == kid:
#                 e = int.from_bytes(self.decode_padding(jwk_data['e']), 'big')
#                 n = int.from_bytes(self.decode_padding(jwk_data['n']), 'big')
#                 return RSAPublicNumbers(e, n).public_key(default_backend())
#         raise Exception('Public key not found')
#
#     def decode_token(self, token, auth0_domain, api_identifier):
#         header = jwt.get_unverified_header(token)
#         public_key = self.get_public_key(auth0_domain, header['kid'])
#
#         return jwt.decode(
#             token,
#             public_key,
#             algorithms=['RS256'],
#             audience=api_identifier
#         )
#
#     def __call__(self, request):
#         # Extract the tenant from the Auth0 token payload
#         auth_header = request.headers.get('Authorization')
#         if auth_header:
#             _, token = auth_header.split()
#             try:
#                 payload = self.decode_token(token, config.AUTH0_DOMAIN, config.AUTH0_API_IDENTIFIER)
#                 print(payload)
#                 # payload = jose.jwt.decode(
#                 #     token, config.AUTH0_CLIENT_SECRET,
#                 #     algorithms=['RS256'],
#                 #     audience=config.AUTH0_API_IDENTIFIER
#                 # )
#                 # tenant_id = payload.get("https://your-namespace/tenant_id")
#                 # tenant = Tenant.objects.get(auth0_tenant_id=tenant_id)
#                 # request.tenant = tenant
#             except Tenant.DoesNotExist:
#                 request.tenant = None
#
#         response = self.get_response(request)
#         return response
