from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from . import serializers
from functools import wraps
from rest_framework.decorators import api_view
import jwt
from django.http import JsonResponse
from rest_framework.decorators import permission_classes

User = get_user_model()


def get_token_auth_header(request):
    # print(request.META)
    auth = request.META.get("AUTH0_CLIENT_SECRET", None)
    # print(auth)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response

        return decorated

    return require_scope


class AccountCreate(generics.CreateAPIView):
    name = 'account-create'
    serializer_class = serializers.AccountSerializer
    permission_classes = (
        permissions.AllowAny,
    )


class UserList(generics.ListCreateAPIView):
    name = 'user-list'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        tenant_id = self.request.user.tenant_id
        serializer.save(tenant_id=tenant_id)

    def get_queryset(self):
        tenant_id = self.request.user.tenant_id
        return super().get_queryset().filter(tenant_id=tenant_id)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'user-detail'
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        tenant_id = self.request.user.tenant_id
        return super().get_queryset().filter(tenant_id=tenant_id)


class TenantDetail(generics.RetrieveUpdateAPIView):
    name = 'tenant-detail'
    permissions = (
        requires_scope('write:messes')
    )
    serializer_class = serializers.TenantSerializer

    def get_object(self):
        return self.request.user.tenant


@api_view(['GET'])
@requires_scope('read:messages')
def test_scoped(request):
    return JsonResponse({
        'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.'})
