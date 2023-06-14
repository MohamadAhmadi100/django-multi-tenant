import consul
from dotenv import load_dotenv
import os
import base64
from django.core.cache import cache

load_dotenv()


class Setting:
    def __init__(self):
        self.CONSUL_HOST = os.getenv("CONSUL_HOST")
        self.CONSUL_PORT = os.getenv("CONSUL_PORT")
        self.CONSUL_TOKEN = os.getenv("CONSUL_TOKEN")
        self.DEBUG: bool = True if os.getenv("DEBUG_MODE") == "true" else False
        self.SECRET_KEY: str = os.getenv('SECRET_KEY')
        self.variables = dict()
        # auth0
        self.AUTH0_CLIENT_ID = None
        self.AUTH0_CLIENT_SECRET = None
        self.AUTH0_AUDIENCE = None
        self.AUTH0_AUTHORIZATION_URL = None
        self.AUTH0_JWKS_URL = None
        self.AUTH0_MANAGEMENT_ORGANIZATION_KEY = None
        self.AUTH0_TOKEN_URL = None
        self.AUTH0_CALLBACK_URL = None
        self.AUTH0_LOGIN_URL = None
        self.AUTH0_LOGOUT_URL = None
        # database
        self.DATABASE_NAME = None
        self.DATABASE_USER = None
        self.DATABASE_PASSWORD = None
        self.DATABASE_HOST = None
        self.DATABASE_PORT = None
        # sentry
        self.SENTRY_DSN = None

    def request_consul(self):
        consul_client = consul.Consul(
            host=self.CONSUL_HOST,
            port=self.CONSUL_PORT,
            token=self.CONSUL_TOKEN,
            scheme="https",
            verify=True)
        index, data = consul_client.kv.get(key="", recurse=True)
        return index, data

    def convert_to_dict(self, index, data):
        for item in data:
            key = item['Key']
            value = item['Value']
            if value:
                value = value.decode('utf-8')
                if type(value) == bytes:
                    value += '=' * ((4 - len(value) % 4) % 4)
                    value = base64.b64decode(value)
            self.variables[key] = value
        return self.variables

    def set_values(self):
        # auth0
        self.AUTH0_CLIENT_ID = self.variables.get("Spov/Authentication/CLIENT_ID", None)
        self.AUTH0_CLIENT_SECRET = self.variables.get("Spov/Authentication/CLIENT_SECRET", None)
        self.AUTH0_AUDIENCE = self.variables.get("Spov/Authentication/AUDIENCE", None)
        self.AUTH0_AUTHORIZATION_URL = self.variables.get("Spov/Authentication/AUTHORIZATION_URL", None)
        self.AUTH0_JWKS_URL = self.variables.get("Spov/Authentication/JWKS_URL", None)
        self.AUTH0_MANAGEMENT_ORGANIZATION_KEY = self.variables.get("Spov/Authentication/MANAGEMENT_ORGANIZATION_KEY",
                                                                    None)
        self.AUTH0_TOKEN_URL = self.variables.get("Spov/Authentication/TOKEN_URL", None)
        self.AUTH0_CALLBACK_URL = self.variables.get("Spov/Authentication/CALLBACK_URL", None)
        self.AUTH0_LOGIN_URL = self.variables.get("Spov/Authentication/LOGIN_URL", None)
        self.AUTH0_LOGOUT_URL = self.variables.get("Spov/Authentication/LOGOUT_URL", None)
        # database
        self.DATABASE_NAME = self.variables.get("Spov/Database/NAME", None)
        self.DATABASE_USER = self.variables.get("Spov/Database/USERNAME", None)
        self.DATABASE_PASSWORD = self.variables.get("Spov/Database/PASSWORD", None)
        self.DATABASE_HOST = self.variables.get("Spov/Database/HOST", None)
        self.DATABASE_PORT = self.variables.get("Spov/Database/PORT", 5432)
        self.SENTRY_DSN = self.variables.get("Spov/Sentry/API_DSN", None)

    def refresh_variables(self):
        index, data = self.request_consul()
        return self.convert_to_dict(index, data)

    def get_new_settings(self):
        self.refresh_variables()
        self.set_values()
        self.set_cache()

    def set_cache(self):
        cache.set("variables", self.variables, 86400)

    def get_cached_configs(self):
        variables = cache.get("variables")
        if not variables:
            self.get_new_settings()
        else:
            self.variables = variables
        api_output = dict()
        for k, v in self.variables.items():
            if "Database" in k:  # or "CLIENT_SECRET" in k
                continue
            api_output[k] = v
        return api_output


setting = Setting()
if __name__ == '__main__':
    setting.get_new_settings()
    # setting.get_cache()
