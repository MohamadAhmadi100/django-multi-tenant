from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from . import serializers

User = get_user_model()


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
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = serializers.TenantSerializer

    def get_object(self):
        return self.request.user.tenant
