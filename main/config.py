import consul
from dotenv import load_dotenv
import os
import base64

load_dotenv()

CONFIG_VALID_KEYS = ["Authentication/AUDIENCE", "Authentication/AUTHORIZATION_URL", "Authentication/CLIENT_ID",
                     "Authentication/CLIENT_SECRET", "Authentication/JWKS_URL",
                     "Authentication/MANAGEMENT_ORGANIZATION_KEY", "Authentication/TOKEN_URL", "Database/DatabaseName",
                     "Database/Host", "Database/Pass", "Database/User"]


class Setting:
    CONSUL_HOST: str = os.getenv("CONSUL_HOST")
    CONSUL_PORT: str = os.getenv("CONSUL_PORT")
    CONSUL_TOKEN: str = os.getenv("CONSUL_TOKEN")
    DEBUG: bool = True if os.getenv("DEBUG_MODE") == "true" else False
    SECRET_KEY: str = os.getenv('SECRET_KEY')

    # auth0
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID: str = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET: str = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_API_IDENTIFIER: str = os.getenv("AUTH0_API_IDENTIFIER")
    AUTH0_MANAGEMENT_API_CLIENT_ID: str = os.getenv("AUTH0_MANAGEMENT_API_CLIENT_ID")
    AUTH0_MANAGEMENT_API_CLIENT_SECRET: str = os.getenv("AUTH0_MANAGEMENT_API_CLIENT_SECRET")
    AUTH0_CALLBACK_URL: str = os.getenv("AUTH0_CALLBACK_URL")
    # database
    DATABASE_NAME: str = os.getenv('DATABASE_NAME')
    DATABASE_USER: str = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD: str = os.getenv('DATABASE_PASSWORD')
    DATABASE_HOST: str = os.getenv('DATABASE_HOST')
    DATABASE_PORT: int = int(os.getenv('DATABASE_PORT'))


setting = Setting()

# centry
SENTRY_DSN = "https://efa604a455114b499ed8bea6c322eb70@o4505311396102144.ingest.sentry.io/4505311403376640"


class ConsulConfigs:
    def __init__(self):
        self.CONSUL_HOST = setting.CONSUL_HOST
        self.CONSUL_PORT = setting.CONSUL_PORT
        self.CONSUL_TOKEN = setting.CONSUL_TOKEN
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
                    print(value)
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
        self.DATABASE_NAME = self.variables.get("Spov/Database/DatabaseName", None)
        self.DATABASE_USER = self.variables.get("Spov/Database/User", None)
        self.DATABASE_PASSWORD = self.variables.get("Spov/Database/Pass", None)
        self.DATABASE_HOST = self.variables.get("Spov/Database/Host", None)
        self.DATABASE_PORT = self.variables.get("Spov/Database/Host", 5432)

    def refresh_variables(self):
        index, data = self.request_consul()
        return self.convert_to_dict(index, data)

    def get_settings(self):
        self.refresh_variables()
        self.set_values()
        print(self.DATABASE_NAME)

    def set_cache(self):
        ...

    def get_cache(self):
        ...


a = ConsulConfigs()
a.get_settings()

