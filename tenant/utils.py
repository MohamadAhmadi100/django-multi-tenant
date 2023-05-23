import json
import os

from django.contrib.auth import authenticate
import jwt
import requests
from django.conf import settings
from six.moves.urllib import request


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    # auth0_domain = os.environ.get('AUTH0_DOMAIN')
    # jwks = requests.get('https://{}/.well-known/jwks.json'.format(auth0_domain)).json()
    jsonurl = request.urlopen(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    api_identifier = os.environ.get('API_IDENTIFIER')
    issuer = f'https://{settings.AUTH0_DOMAIN}/'
    return jwt.decode(token, public_key, audience=api_identifier, issuer=issuer, algorithms=['RS256'])
# import uuid
# import warnings
# from calendar import timegm
# from datetime import datetime
# from functools import wraps
#
# import jwt
# from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
# from django.http import JsonResponse
# from rest_framework_simplejwt.settings import api_settings
#
# User = get_user_model()
#
#
# def get_username(jwt):
#     username = jwt.get('username')
#     tenant = jwt.get('https://next-ocr.io/tenant')
#     authenticate(remote_user=username, tenant=tenant)
#     return username
#
#
# def jwt_payload_handler(user):
#     username_field = User.USERNAME_FIELD
#     username = get_username(user)
#
#     warnings.warn(
#         'The following fields will be removed in the future: '
#         '`email` and `user_id`. ',
#         DeprecationWarning
#     )
#
#     payload = {
#         'user_id': user.pk,
#         'tenant_id': user.tenant_id,
#         'username': username,
#         'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
#     }
#     if hasattr(user, 'email'):
#         payload['email'] = user.email
#     if isinstance(user.pk, uuid.UUID):
#         payload['user_id'] = str(user.pk)
#     if isinstance(user.tenant_id, uuid.UUID):
#         payload['user_id'] = str(user.tenant_id)
#
#     payload[username_field] = username
#
#     if api_settings.JWT_ALLOW_REFRESH:
#         payload['orig_iat'] = timegm(
#             datetime.utcnow().utctimetuple()
#         )
#
#     if api_settings.JWT_AUDIENCE is not None:
#         payload['aud'] = api_settings.JWT_AUDIENCE
#
#     if api_settings.JWT_ISSUER is not None:
#         payload['iss'] = api_settings.JWT_ISSUER
#
#     return payload
#
#
# def jwt_decode_handler(token):
#     jwt_ = jwt.decode(token, verify=False)
#     return jwt_
#
#
# def jwt_get_secret_key(payload=None):
#     if api_settings.JWT_GET_USER_SECRET_KEY:
#         User = get_user_model()  # noqa: N806
#         user = User.objects.get(pk=payload.get('user_id'))
#         key = str(api_settings.JWT_GET_USER_SECRET_KEY(user))
#         return key
#     return api_settings.JWT_SECRET_KEY
#
#
# class JWTManager:
#
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def get_token_auth_header(request):
#         auth = request.META.get("HTTP_AUTHORIZATION", None)
#         token = auth.split()[1]
#         return token
#
#     @staticmethod
#     def requires_scope(required_scope):
#         def require_scope(f):
#             @wraps(f)
#             def decorated(*args, **kwargs):
#                 token = JWTManager.get_token_auth_header(args[0])
#                 unverified_claims = jwt.get_unverified_claims(token)
#                 token_scopes = unverified_claims["scope"].split()
#                 for token_scope in token_scopes:
#                     if token_scope == required_scope:
#                         return f(*args, **kwargs)
#                 response = JsonResponse({'message': 'You don\'t have access to this resource'})
#                 response.status_code = 403
#                 return response
#
#             return decorated
#
#         return require_scope
