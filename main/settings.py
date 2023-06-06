import json
import os
import textwrap
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate
from dotenv import load_dotenv
from six.moves.urllib import request
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()
# auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_API_IDENTIFIER = os.getenv("AUTH0_API_IDENTIFIER")
AUTH0_MANAGEMENT_API_CLIENT_ID = os.getenv("AUTH0_MANAGEMENT_API_CLIENT_ID")
AUTH0_MANAGEMENT_API_CLIENT_SECRET = os.getenv("AUTH0_MANAGEMENT_API_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")

# database
DATABASE_NAME = os.getenv('DATABASE_NAME'),
DATABASE_USER = os.getenv('DATABASE_USER'),
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD'),
DATABASE_HOST = os.getenv('DATABASE_HOST'),
DATABASE_PORT = os.getenv('DATABASE_PORT'),

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-_(yu5o^u(2vzksw+a6emtat8m+qnk-3$p6f1=1-nbv+vl_0-)*'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party apps
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    'drf_yasg',
    'rest_framework_simplejwt',

    # apps
    'tenant.apps.TenantConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'DRF Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'tenant.User'

WSGI_APPLICATION = 'main.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'main_test',
        'USER': 'maintest',
        'PASSWORD': 'adminadmin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

AUTHENTICATION_BACKENDS = [
    'tenant.auth_backends.Auth0Backend',

]
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

}
IMPORT_STRINGS = (
    'JWT_ENCODE_HANDLER',
    'JWT_DECODE_HANDLER',
    'JWT_PAYLOAD_HANDLER',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER',
    'JWT_PAYLOAD_GET_USERNAME_HANDLER',
    'JWT_RESPONSE_PAYLOAD_HANDLER',
    'JWT_GET_USER_SECRET_KEY',
)

jsonurl = request.urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
jwks = json.loads(jsonurl.read())
t = textwrap.fill(jwks['keys'][0]['x5c'][0])
CERT = '-----BEGIN CERTIFICATE-----\n' + textwrap.fill(jwks['keys'][0]['x5c'][0], 64) + '\n-----END CERTIFICATE-----'
CERTIFICATE = load_pem_x509_certificate(str.encode(CERT), default_backend())
PUBLICKEY = CERTIFICATE.public_key()

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_IDENTIFIER = os.environ.get('AUTH0_API_IDENTIFIER')
PUBLIC_KEY = None
JWT_ISSUER = None

if AUTH0_DOMAIN:
    JWT_ISSUER = 'https://' + AUTH0_DOMAIN + '/'

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'auth0authorization.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'auth0authorization.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': API_IDENTIFIER,
    'JWT_ISSUER': JWT_ISSUER,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

# sentry

sentry_sdk.init(
    dsn="https://efa604a455114b499ed8bea6c322eb70@o4505311396102144.ingest.sentry.io/4505311403376640",
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)
