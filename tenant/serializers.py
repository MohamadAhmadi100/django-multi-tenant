from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tenant

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        updated = super().update(instance, validated_data)

        if 'password' in validated_data:
            updated.set_password(validated_data['password'])
            updated.save()
        return updated


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

# from rest_framework import serializers
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
