from pathlib import Path
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .config import setting

setting.get_cached_configs()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = setting.SECRET_KEY
DEBUG = setting.DEBUG

ALLOWED_HOSTS = ["*"]

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
    'consul',
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


WSGI_APPLICATION = 'main.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': setting.DATABASE_NAME,
        'USER': setting.DATABASE_USER,
        'PASSWORD': setting.DATABASE_PASSWORD,
        'HOST': setting.DATABASE_HOST,
        'PORT': setting.DATABASE_PORT,
        'OPTIONS': {
            'sslmode': 'require',
            'sslrootcert': os.path.join(BASE_DIR, 'certificate/server-ca.pem'),
            'sslcert': os.path.join(BASE_DIR, 'certificate/client-cert.pem'),
            'sslkey': os.path.join(BASE_DIR, 'certificate/client-key.pem'),
        },
        "default": {
            "CONN_MAX_AGE": 1800
        }
    }
}
DATABASE_ROUTERS = ['tenant.router.OrganizationDatabaseRouter']

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
        'tenant.auth0authentication.Auth0JSONWebTokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    # 'EXCEPTION_HANDLER': 'tenant.exception_handler.custom_exception_handler',

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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ORIGIN_ALLOW_ALL = True

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Media Settings
MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')


# sentry
sentry_sdk.init(
    dsn=setting.SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True
)
