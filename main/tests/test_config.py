from collections import defaultdict
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core import mail
from main.config import Setting


@pytest.fixture(autouse=True)
def enable_email_capturing():
    mail.outbox = []


@pytest.fixture(autouse=True)
def django_settings():
    if not settings.configured:
        settings.configure()


@pytest.fixture
def setting_instance():
    return Setting()


@patch("main.config.consul.Consul")
def test_request_consul(mock_consul, setting_instance):
    mock_consul_instance = mock_consul.return_value
    mock_consul_instance.kv.get.return_value = ("index", [{"Key": "key", "Value": "dmFsdWU="}])

    index, data = setting_instance.request_consul()

    assert index == "index"
    assert data == [{"Key": "key", "Value": "dmFsdWU="}]
    mock_consul_instance.kv.get.assert_called_once_with(key="", recurse=True)


def test_set_values(setting_instance):
    setting_instance.variables = {
        "Spov/Authentication/CLIENT_ID": "client_id",
        "Spov/Authentication/CLIENT_SECRET": "client_secret",
        "Spov/Authentication/AUDIENCE": "audience",
    }

    setting_instance.set_values()

    assert setting_instance.AUTH0_CLIENT_ID == "client_id"
    assert setting_instance.AUTH0_CLIENT_SECRET == "client_secret"
    assert setting_instance.AUTH0_AUDIENCE == "audience"


def test_convert_to_dict(setting_instance):
    d = defaultdict(lambda: defaultdict(dict))
    d["key1"]["key2"]["key3"] = "value"

    result = setting_instance.convert_to_dict(d)

    assert result == {"key1": {"key2": {"key3": "value"}}}


# @patch("main.config.redis")
# def test_get_client_response(mock_cache, setting_instance):
#     mock_cache.get.return_value = {
#         "Spov/Authentication/CLIENT_ID": "client_id",
#         "Spov/Authentication/CLIENT_SECRET": "client_secret",
#         "Spov/Authentication/AUDIENCE": "audience",
#     }
#
#     result = setting_instance.get_client_response()
#
#     assert result == {
#         "Spov": {
#             "Authentication": {
#                 "CLIENT_ID": "client_id",
#                 "CLIENT_SECRET": "client_secret",
#                 "AUDIENCE": "audience",
#             }
#         }
#     }
