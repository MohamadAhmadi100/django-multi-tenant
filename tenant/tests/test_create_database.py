import os
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pytest
from django.conf import settings
from django.core import mail
from main.config import Setting
from tenant.management.commands.create_database import OrganizationDatabaseManager


@pytest.fixture(autouse=True)
def enable_email_capturing():
    mail.outbox = []


@pytest.fixture(autouse=True, scope="session")
def django_settings():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings'
    import django
    django.setup()


@pytest.fixture
def setting_instance():
    return Setting()


os.environ.setdefault('DJANGO_SETTINGS_MODULE', Setting)


class OrganizationDatabaseManagerTest(TestCase):

    @patch("tenant.management.commands.create_database.psycopg2.connect")
    def test_connect_success(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        manager = OrganizationDatabaseManager()

        with patch.object(manager.logger, 'info') as mock_logger_info:
            connection = manager.connect('testdb')

            self.assertEqual(connection, mock_connection)
            mock_logger_info.assert_called_with("Connected to database testdb successfully.")

    @patch("tenant.management.commands.create_database.psycopg2.connect")
    def test_connect_failure(self, mock_connect):
        mock_connect.side_effect = Exception("Database connection error")

        manager = OrganizationDatabaseManager()

        with patch.object(manager.logger, 'error') as mock_logger_error:
            connection = manager.connect('testdb')

            self.assertIsNone(connection)
            mock_logger_error.assert_called_with("Error connecting database testdb: Database connection error")

    @patch("tenant.management.commands.create_database.psycopg2.connect")
    @patch.object(OrganizationDatabaseManager, 'connect')
    def test_create_organization_database(self, mock_connect_method, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect_method.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        manager = OrganizationDatabaseManager()
        manager.connection = mock_connection

        with patch.object(manager.logger, 'info') as mock_logger_info:
            manager.create_organization_database('org-test')

            mock_logger_info.assert_any_call("Database org-test created successfully.")
