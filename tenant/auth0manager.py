import requests
from main.config import setting

setting.get_cached_configs()


class Auth0:
    def __init__(self):
        self.AUTH0_CLIENT_ID = setting.AUTH0_CLIENT_ID
        self.AUTH0_CLIENT_SECRET = setting.AUTH0_CLIENT_SECRET
        self.AUTH0_AUDIENCE = setting.AUTH0_AUDIENCE
        self.AUTH0_TOKEN_URL = setting.AUTH0_TOKEN_URL
        self.grant_type = "client_credentials"

    def get_management_api_token(self):
        payload = {
            'client_id': self.AUTH0_CLIENT_ID,
            'client_secret': self.AUTH0_CLIENT_SECRET,
            'audience': self.AUTH0_AUDIENCE,
            'grant_type': 'client_credentials'
        }
        response = requests.post(self.AUTH0_TOKEN_URL, json=payload)
        return response.json().get('access_token')
