import json
import jwt
import requests
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
from .auth0manager import Auth0


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


class ListUsersView(APIView):
    def get(self, request):
        id_token = request.headers.get('Authorization').split(' ')[1]
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        # roles = decoded_token.get()  # NAMESPACE + 'roles', [])
        # print(decoded_token)

        if 'Manager' in "Manager":
            management_access_token = Auth0().get_management_api_token()
            setting.get_cached_configs()
            response = requests.get(f'https://dev-d6tfpiyvod1zdqiv.us.auth0.com/api/v2/users',
                                    headers={'Authorization': f'Bearer {management_access_token}'})
            return Response(response.json())
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


# class RetrieveUserView(APIView):
#     def get(self, request, user_id):
#         id_token = request.headers.get('Authorization').split(' ')[1]
#         decoded_token = jwt.decode(id_token, options={"verify_signature": False})
#         roles = decoded_token.get(NAMESPACE + 'roles', [])
#
#         if 'Manager' in roles:
#             access_token = get_management_api_token()
#             response = requests.get(f'https://{AUTH0_DOMAIN}/api/v2/users/{user_id}',
#                                     headers={'Authorization': f'Bearer {access_token}'})
#             return Response(response.json())
#         else:
#             return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


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
