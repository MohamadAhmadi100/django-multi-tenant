import requests
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import JsonResponse
import json
from django.conf import settings
from auth0.authentication import GetToken


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


class UserRegistrationView(APIView):
    def post(self, request):
        trigger_error(request)
        data = {
            'email': request.data.get('email'),
            'password': request.data.get('password'),
        }
        response = requests.post(
            f'https://{settings.AUTH0_DOMAIN}/api/v2/users',
            headers={'Authorization': f'Bearer {settings.AUTH0_CLIENT_SECRET}'},
            json=data
        )
        return Response(response.json(), status=response.status_code)


@api_view(['GET'])
@permission_classes([IsAuthenticated, CustomPermission])
def protected_view(request):
    return Response({'message': 'token Bearer'})
