import requests
import sentry_sdk
from main.config import setting
from rest_framework import permissions
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization, MainUser
from .serializers import OrganizationSerializer, MainUserSerializer


class ListUsersView(APIView):
    def get(self, request):
        try:
            organization_id = request.organization_id
            organization = Organization.objects.filter(organization_id=organization_id).first()
            if not organization:
                return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
            users = organization.users.all()
            serializer = MainUserSerializer(users, many=True)
            return Response(serializer.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RetrieveUserView(APIView):
    def get(self, request):
        try:
            organization_id = request.organization_id
            user_id = request.user_id
            organization = Organization.objects.filter(organization_id=organization_id).first()
            if not organization:
                return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
            user = MainUser.objects.filter(user_id=user_id, organization=organization).first()
            if not user:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = MainUserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RetrieveOrganizationView(APIView):
    def get(self, request):
        try:
            organization_id = request.organization_id
            organization = Organization.objects.filter(organization_id=organization_id).first()
            if not organization:
                return Response({"error": "Organization not found."}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrganizationSerializer(organization)
            return Response(serializer.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ListOrganizationsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            organizations = Organization.objects.all()
            serializer = OrganizationSerializer(organizations, many=True)
            return Response(serializer.data)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ConfigView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            configs = setting.get_client_response()
            return Response(configs, status=status.HTTP_200_OK)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class RefreshConsulConfigView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            setting.get_new_settings()
            return Response({'message': 'OK'}, status=status.HTTP_200_OK)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class GetUserDetailsFromAuth0(APIView):

    def get(self, request):
        try:
            access_token = request.headers.get('Authorization')

            if not access_token:
                return Response({"error": "Authorization header is required"}, status=status.HTTP_400_BAD_REQUEST)

            auth0_domain = setting.AUTH0_JWKS_URL.split("/")[2]
            auth0_userinfo_url = f'https://{auth0_domain}/userinfo'
            response = requests.get(auth0_userinfo_url, headers={'Authorization': access_token})

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                return Response(response.json(), status=response.status_code)
        except Exception as e:
            sentry_sdk.capture_exception(e)
            return Response({'error': e.args}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
