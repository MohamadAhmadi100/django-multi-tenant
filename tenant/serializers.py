from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Tenant

User = get_user_model()


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['name', 'auth0_tenant_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class TenantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tenant
        fields = (
            'id',
            'name',
            'address',
        )


class AccountSerializer(serializers.Serializer):
    tenant = TenantSerializer()
    user = UserSerializer()

    def create(self, validated_data):
        tenant_data = validated_data['tenant']
        user_data = validated_data['user']

        tenant, user = Tenant.objects.create_account(
            tenant_name=tenant_data.get('name'),
            tenant_address=tenant_data.get('address'),
            username=user_data.get('username'),
            password=user_data.get('password'),
        )

        return {'tenant': tenant, 'user': user}

    def update(self, instance, validated_data):
        raise NotImplementedError('Cannot call update() on an account')
