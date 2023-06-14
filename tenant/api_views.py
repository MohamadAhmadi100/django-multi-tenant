import json

from auth0.authentication import GetToken
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from main.config import setting
from .serializers import TenantSerializer


def trigger_error(request):
    division_by_zero = 1 / 0


class OrganizationDataView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        organization_id = request.user.organization_id
        user_id = request.user.user_id
        data = {"organization_id": organization_id, "user_id": user_id}

        return Response(data)


class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        return 'admin' in request.user.role


class TenantData(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if hasattr(request, 'tenant') and request.tenant:
            serializer = TenantSerializer(request.tenant)
            return Response(serializer.data)
        else:
            return Response({'error': 'Tenant not found'}, status=status.HTTP_404_NOT_FOUND)


class ConfigView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            configs = setting.get_cached_configs()
            return Response({"message": configs}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RefreshConsulConfigView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            setting.get_new_settings()
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
