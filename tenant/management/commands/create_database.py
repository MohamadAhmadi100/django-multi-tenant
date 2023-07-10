import logging
import os

import colorlog
from django.conf import settings
from django.core.management import call_command
from django.db import connections
from django.db.utils import DatabaseError
from main.config import setting
from psycopg2 import sql
import sentry_sdk

setting.get_cached_configs()


class OrganizationDatabaseManager:
    _instance = None
    _handlers_set = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OrganizationDatabaseManager, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def __init__(self):
        self.db_name = setting.DATABASE_NAME
        self.db_user = setting.DATABASE_USER
        self.db_password = setting.DATABASE_PASSWORD
        self.db_host = setting.DATABASE_HOST
        self.connection = None

        self.logger = logging.getLogger("TenantDatabaseManager")
        self.setup_logger()

    def setup_logger(self):
        self.logger.setLevel(logging.DEBUG)
        formatter = colorlog.ColoredFormatter(
            "%(log_color)s [%(levelname)s] [%(asctime)s]  %(reset)s%(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red",
            },
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def connect(self, dbname):
        try:
            dbname = dbname.lower()
            conn_params = {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": dbname,
                "USER": self.db_user,
                "PASSWORD": self.db_password,
                "HOST": self.db_host,
                "PORT": "5432",
                "TIME_ZONE": "UTC",
                "CONN_HEALTH_CHECKS": {
                    "ENABLED": True,
                    "MAX_AGE": 300,
                    "MAX_RETRIES": 5,
                    "RETRY_DELAY": 5,
                },
                "ATOMIC_REQUESTS": True,
                "CONN_MAX_AGE": 10,
                "AUTOCOMMIT": True,
                "OPTIONS": {
                    "sslmode": "require",
                    "sslrootcert": os.path.join(
                        settings.BASE_DIR, "certificate/server-ca.pem"
                    ),
                    "sslcert": os.path.join(
                        settings.BASE_DIR, "certificate/client-cert.pem"
                    ),
                    "sslkey": os.path.join(
                        settings.BASE_DIR, "certificate/client-key.pem"
                    ),
                },
                "default": {"CONN_MAX_AGE": 10},
            }
            connections.databases[dbname] = conn_params
            self.connection = connections[dbname].cursor().connection
            self.logger.info(f"Connected to database {dbname} successfully.")
            return self.connection
        except Exception as error:
            sentry_sdk.capture_exception(error)
            self.logger.error(f"Error connecting to database {dbname}: {error}")
            return None

    def create_organization_database(self, organization_id):
        self.connect(self.db_name)
        with self.connection.cursor() as cursor:
            try:
                organization_id = organization_id.lower()
                cursor.execute(
                    "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
                    (organization_id,),
                )
                exists = cursor.fetchone()
                if not exists:
                    create_database_sql = sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(organization_id)
                    )
                    cursor.execute(create_database_sql)
                    self.logger.info(
                        f"Database {organization_id} created successfully."
                    )
                else:
                    self.logger.info(
                        f"Database {organization_id} already exists. Continuing without creation."
                    )
            except Exception as error:
                if "already exists" in str(error):
                    self.logger.warning(f"Database {organization_id} already exists.")
                else:
                    sentry_sdk.capture_exception(error)
                    self.logger.error(
                        f"Error creating database {organization_id}: {error}"
                    )
            self.connect(organization_id)
            for app in setting.MIGRATION_APPS_LIST:
                try:
                    call_command("migrate", app, database=organization_id)
                    self.logger.info(f"Migrations applied for {organization_id}.")
                except DatabaseError as e:
                    sentry_sdk.capture_exception(e)
                    self.logger.error(f"Error running migrations: {e}")
                except Exception as e:
                    sentry_sdk.capture_exception(e)
                    self.logger.error(f"Error running migrations: {e}")
