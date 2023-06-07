import consul
from dotenv import load_dotenv
import os

load_dotenv()
CONSUL_BACKEND = {
    'HOST': '127.0.0.1',
    'PORT': 8500,  # Consul agent port
    'TOKEN': '',  # Consul ACL token (if enabled)
    'SCHEME': 'http',  # Consul agent connection scheme (http or https)
}


class Config:
    ...


consul_client = consul.Consul(host='127.0.0.1', port=8500)
index, data = consul_client.kv.get('DATABASE_URL')
if data:
    database_url = data['Value'].decode('utf-8')
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

SECRET_KEY = 'django-insecure-_(yu5o^u(2vzksw+a6emtat8m+qnk-3$p6f1=1-nbv+vl_0-)*'

# centry
SENTRY_DSN = "https://efa604a455114b499ed8bea6c322eb70@o4505311396102144.ingest.sentry.io/4505311403376640"
