import auth0
from auth0.authentication import GetToken
from django.conf import settings
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

param = openapi.Parameter('test', openapi.IN_QUERY, type=openapi.TYPE_BOOLEAN)


@swagger_auto_schema(methods=['post'], request_body=UserSerializer)
@api_view(['POST'])
def login(request):
    token = GetToken(domain=settings.AUTH0_DOMAIN, client_id=settings.AUTH0_CLIENT_ID,
                     client_assertion_signing_key=settings.PUBLICKEY, client_assertion_signing_alg="RS256")
    print(token.client_credentials())
    # token.login(username=request.data['username'], password=request.data['password'],
    #             realm="Username-Password-Authentication")
    # print(token.get())
    # credentials = token.client_credentials(settings.AUTH0_API_IDENTIFIER)
    # print(credentials)
    return JsonResponse(dict(message="token"))

# from authlib.integrations.django_oauth2 import ResourceProtector
# from django.http import JsonResponse
# from . import validator
# from django.conf import settings
# from rest_framework.decorators import api_view
# from auth0.authentication import Database
#
# database = Database('my-domain.us.auth0.com', 'my-client-id')
#
# database.signup(email='user@domain.com', password='secr3t', connection='Username-Password-Authentication')
# require_auth = ResourceProtector()
# validator = validator.Auth0JWTBearerTokenValidator(
#     settings.AUTH0_DOMAIN,
#     settings.AUTH0_API_IDENTIFIER
# )
# print(validator)
# require_auth.register_token_validator(validator)
#
#
# def public(request):
#     """No access token required to access this route
#     """
#     response = "Hello from a public endpoint! You don't need to be authenticated to see this."
#     return JsonResponse(dict(message=response))
#
#
# @require_auth(None)
# def private(request):
#     """A valid access token is required to access this route
#     """
#     response = "Hello from a private endpoint! You need to be authenticated to see this."
#     return JsonResponse(dict(message=response))
#
#
# # @api_view(['POST'])
# # def register(request):
# #     ser
# @require_auth("read:messages")
# @api_view(['POST'])
# def private_scoped(request):
#     """A valid access token and an appropriate scope are required to access this route
#     """
#     response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
#     return JsonResponse(dict(message=response))

# from django.contrib.auth import get_user_model
# from rest_framework import generics, permissions
# from . import serializers
# from functools import wraps
# from rest_framework.decorators import api_view
# import jwt
# from django.http import JsonResponse
# from rest_framework.decorators import permission_classes
# from authlib.integrations.django_client import OAuth
#
# User = get_user_model()
# oauth = OAuth()
#
# oauth.register(
#     "auth0",
#     client_id="ZTUapMYK5OnVBdxCTbEu4lRD2JnnPwr8",
#     client_secret="4IqHsHQsnPd_v43y9mS8afwJQ90v5zJ4mNJfXzYq6zNIvFdJFPJroWtaAKePt4lA",
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url="https://dev-rkudueft2tokyrt8.us.auth0.com/.well-known/openid-configuration",
# )
#
#
#
# def get_token_auth_header(request):
#     # print(request.META)
#     auth = request.META.get("AUTH0_CLIENT_SECRET", None)
#     # print(auth)
#     parts = auth.split()
#     token = parts[1]
#
#     return token
#
#
# def requires_scope(required_scope):
#     def require_scope(f):
#         @wraps(f)
#         def decorated(*args, **kwargs):
#             token = get_token_auth_header(args[0])
#             decoded = jwt.decode(token, verify=False)
#             if decoded.get("scope"):
#                 token_scopes = decoded["scope"].split()
#                 for token_scope in token_scopes:
#                     if token_scope == required_scope:
#                         return f(*args, **kwargs)
#             response = JsonResponse({'message': 'You don\'t have access to this resource'})
#             response.status_code = 403
#             return response
#
#         return decorated
#
#     return require_scope
#
#
# class AccountCreate(generics.CreateAPIView):
#     name = 'account-create'
#     serializer_class = serializers.AccountSerializer
#     permission_classes = (
#         permissions.AllowAny,
#     )
#
#
# class UserList(generics.ListCreateAPIView):
#     name = 'user-list'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.UserSerializer
#     queryset = User.objects.all()
#
#     def perform_create(self, serializer):
#         tenant_id = self.request.user.tenant_id
#         serializer.save(tenant_id=tenant_id)
#
#     def get_queryset(self):
#         tenant_id = self.request.user.tenant_id
#         return super().get_queryset().filter(tenant_id=tenant_id)
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     name = 'user-detail'
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     serializer_class = serializers.UserSerializer
#     queryset = User.objects.all()
#
#     def get_queryset(self):
#         tenant_id = self.request.user.tenant_id
#         return super().get_queryset().filter(tenant_id=tenant_id)
#
#
# class TenantDetail(generics.RetrieveUpdateAPIView):
#     name = 'tenant-detail'
#     permissions = (
#         requires_scope('write:messes')
#     )
#
#     serializer_class = serializers.TenantSerializer
#
#     def get_object(self):
#         return self.request.user.tenant
#
#
# @api_view(['GET'])
# # @requires_scope('read:messages')
# def test_scoped(request):
#     token = oauth.auth0.authorize_access_token(request)
#     print(token)
#     return JsonResponse({
#         'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.'})
