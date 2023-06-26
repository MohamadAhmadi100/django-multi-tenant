import base64
import os
from collections import defaultdict
from pathlib import Path

import consul
from django.core.cache import cache
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


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
        self.DATABASE_CLIENT_CERT = self.variables.get("Spov/Database/CLIENT_CERT", None)
        self.DATABASE_CLIENT_CERT_PATH = None
        self.DATABASE_CLIENT_KEY = self.variables.get("Spov/Database/CLIENT_KEY", None)
        self.DATABASE_CLIENT_KEY_PATH = None
        self.DATABASE_SERVER_CA = self.variables.get("Spov/Database/SERVER_CA", None)
        self.DATABASE_SERVER_CA_PATH = None
        # sentry
        self.SENTRY_DSN = None
        self.MIGRATION_APPS_LIST = ["tenant"]

    def create_certificate_files(self):
        with open(self.DATABASE_SERVER_CA_PATH, "wb") as ca_cert_file:
            ca_cert_file.write(self.DATABASE_SERVER_CA.encode("UTF-8"))
        os.chmod(self.DATABASE_SERVER_CA_PATH, 0o600)

        with open(self.DATABASE_CLIENT_CERT_PATH, "wb") as client_cert_file:
            client_cert_file.write(self.DATABASE_CLIENT_CERT.encode("UTF-8"))
        os.chmod(self.DATABASE_CLIENT_CERT_PATH, 0o600)

        with open(self.DATABASE_CLIENT_KEY_PATH, "wb") as client_key_file:
            client_key_file.write(self.DATABASE_CLIENT_KEY.encode("UTF-8"))
        os.chmod(self.DATABASE_CLIENT_KEY_PATH, 0o600)

    def request_consul(self):
        consul_client = consul.Consul(
            host=self.CONSUL_HOST,
            port=self.CONSUL_PORT,
            token=self.CONSUL_TOKEN,
            scheme="https",
            verify=True)
        index, data = consul_client.kv.get(key="", recurse=True)
        return index, data

    def convert_binary_to_dict(self, index, data):
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
        self.DATABASE_CLIENT_CERT = self.variables.get("Spov/Database/CLIENT_CERT", None)
        self.DATABASE_CLIENT_CERT_PATH = os.path.join(BASE_DIR, 'certificate/client-cert.pem')
        self.DATABASE_CLIENT_KEY = self.variables.get("Spov/Database/CLIENT_KEY", None)
        self.DATABASE_CLIENT_KEY_PATH = os.path.join(BASE_DIR, 'certificate/client-key.pem')
        self.DATABASE_SERVER_CA = self.variables.get("Spov/Database/SERVER_CA", None)
        self.DATABASE_SERVER_CA_PATH = os.path.join(BASE_DIR, "certificate/server-ca.pem")

        self.SENTRY_DSN = self.variables.get("Spov/Sentry/API_DSN", None)

    def refresh_variables(self):
        index, data = self.request_consul()
        return self.convert_binary_to_dict(index, data)

    def get_new_settings(self):
        self.refresh_variables()
        self.set_values()
        self.create_certificate_files()
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

    def convert_to_dict(self, d):
        if isinstance(d, defaultdict):
            d = {k: self.convert_to_dict(v) for k, v in d.items()}
        return d

    def get_client_response(self):
        variables = self.get_cached_configs()
        api_output = defaultdict(lambda: defaultdict(dict))
        for key, value in variables.items():
            if not value:
                continue

            split_key = key.split('/')
            if len(split_key) < 3:
                continue

            first_level_key, second_level_key, third_level_key = split_key
            api_output[first_level_key][second_level_key][third_level_key] = value

        # Convert defaultdict back to regular dict for cleaner output
        return self.convert_to_dict(api_output)


setting = Setting()
if __name__ == '__main__':
    setting.get_new_settings()
