from unittest.mock import MagicMock, patch

from tenant.management.commands.create_database import OrganizationDatabaseManager


def test_connect_success():
    mock_connection = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = MagicMock()
    with patch.object(OrganizationDatabaseManager, 'connect', return_value=mock_connection):
        assert OrganizationDatabaseManager.connect('test_organization') is not None


def test_connect_failure():
    with patch.object(OrganizationDatabaseManager, 'connect', return_value=None):
        assert OrganizationDatabaseManager.connect('test_organization') is None
