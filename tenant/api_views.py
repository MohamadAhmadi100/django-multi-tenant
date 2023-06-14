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


@api_view(['POST'])
def login(request):
    trigger_error(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            auth0_domain = settings.AUTH0_DOMAIN
            auth0_client_id = settings.AUTH0_CLIENT_ID
            auth0_client_secret = settings.AUTH0_CLIENT_SECRET

            auth0 = GetToken(domain=auth0_domain, client_id=auth0_client_id)
            token_info = auth0.login(
                username,
                password,
                audience=f'https://{auth0_domain}/api/v2/',
                scope='openid profile email',
            )

            access_token = token_info['access_token']
            id_token = token_info['id_token']
            expires_in = token_info['expires_in']

            return JsonResponse({
                'access_token': access_token,
                'id_token': id_token,
                'expires_in': expires_in
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


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
