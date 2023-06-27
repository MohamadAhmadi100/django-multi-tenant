import logging
import os
from time import strftime, localtime

import colorlog
from django.conf import settings
from django.core.management import call_command
from django.db import connections
from django.db.utils import DatabaseError
from main.config import setting
from psycopg2 import sql

setting.get_cached_configs()


class OrganizationDatabaseManager:
    _instance = None
    _handlers_set = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrganizationDatabaseManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.db_name = setting.DATABASE_NAME
        self.db_user = setting.DATABASE_USER
        self.db_password = setting.DATABASE_PASSWORD
        self.db_host = setting.DATABASE_HOST
        self.connection = None

        # Set up logger
        self.now = str(strftime("%Y-%m-%d %H:%M:%S", localtime())).replace(" ", "-")
        self.logger = logging.getLogger('TenantDatabaseManager')
        self.logger.setLevel(logging.DEBUG)

        # Set up colored logs
        if not OrganizationDatabaseManager._handlers_set:
            cformat = "%(log_color)s [%(levelname)s] [%(asctime)s]  %(reset)s%(message)s"
            colors = {'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'red'}
            formatter = colorlog.ColoredFormatter(cformat, log_colors=colors)

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

            # File handler
            file_handler = logging.FileHandler('organization_database_manager.log')
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            OrganizationDatabaseManager._handlers_set = True

    def __enter__(self, db_name=None):
        db_name = db_name if db_name else self.db_name
        self.connect(db_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.logger.info("Database connection pooling set")

    def connect(self, dbname):
        try:
            dbname = dbname.lower()
            settings.DATABASES[dbname] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': dbname,
                'USER': self.db_user,
                'PASSWORD': self.db_password,
                'HOST': self.db_host,
                'PORT': '',
                'TIME_ZONE': 'UTC',
                'CONN_HEALTH_CHECKS': {
                    'ENABLED': True,
                    'MAX_AGE': 300,
                    'MAX_RETRIES': 5,
                    'RETRY_DELAY': 5
                },
                "ATOMIC_REQUESTS": True,
                'CONN_MAX_AGE': 1800,
                'AUTOCOMMIT': True,
                'OPTIONS': {
                    'sslmode': 'require',
                    'sslrootcert': os.path.join(settings.BASE_DIR, 'certificate/server-ca.pem'),
                    'sslcert': os.path.join(settings.BASE_DIR, 'certificate/client-cert.pem'),
                    'sslkey': os.path.join(settings.BASE_DIR, 'certificate/client-key.pem'),
                },
                "default": {
                    "CONN_MAX_AGE": 1800
                }
            }
            self.logger.info(f"Connected to database {dbname} successfully.")
        except Exception as error:
            self.logger.error(f"Error connecting database {dbname}: {error}")
            return None

    def create_organization_database(self, organization_id):
        if self.connection is None:
            self.logger.error("No database connection established")
            return
        cursor = self.connection.cursor()
        try:
            organization_id = organization_id.lower()
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (organization_id,))
            exists = cursor.fetchone()
            if not exists:
                create_database_sql = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(organization_id))
                cursor.execute(create_database_sql)
                self.logger.info(f"Database {organization_id} created successfully.")
            else:
                self.logger.info(f"Database {organization_id} already exists. Continuing without creation.")
        except Exception as error:
            if "already exists" in str(error):
                self.logger.warning(f"Database {organization_id} already exists.")
            else:
                self.logger.error(f"Error creating database {organization_id}: {error}")
        self.connect(organization_id)
        for app in setting.MIGRATION_APPS_LIST:
            try:
                call_command('migrate', app, database=organization_id)
                self.logger.info(f"Migrations applied for {organization_id}.")
            except DatabaseError as e:
                self.logger.error(f"Error running migrations: {e}")
            finally:
                cursor.close()
        connections.close_all()


if __name__ == "__main__":
    with OrganizationDatabaseManager() as manager:
        manager.create_organization_database("new_organization_db")
