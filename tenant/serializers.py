from rest_framework import serializers

from .models import Organization, MainUser


class MainUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = ['user_id', 'created_at', 'active']


class OrganizationSerializer(serializers.ModelSerializer):
    users = MainUserSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = ['name', 'organization_id', 'created_at', 'users']
