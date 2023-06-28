# import pytest
# from main import settings
# from django.core import mail
# from main.config import setting
# import unittest.mock as mock
# from rest_framework.test import APIClient
# from django.test import override_settings
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIRequestFactory
# from unittest.mock import patch
# from tenant.models import Organization, MainUser
# from tenant.api_views import ListUsersView
#
#
# @pytest.fixture
# def client():
#     return APIClient()
#
#
# @pytest.fixture(autouse=True)
# def enable_email_capturing():
#     mail.outbox = []
#
#
# @pytest.fixture(autouse=True)
# def mock_django_db_setup(request, django_db_setup):
#     pass  # mock setup database by pass
#
#
# @pytest.fixture
# def setting_instance():
#     return settings()
#
#
# @pytest.fixture(autouse=True)
# def mock_setting():
#     with mock.patch("tenant.models.setting", setting):
#         yield setting
#
#
# pytestmark = pytest.mark.django_db
#
#
# @pytest.mark.django_db
# class ListUsersViewTest(TestCase):
#     pytestmark = pytest.mark.django_db
#
#     def setUp(self):
#         self.factory = APIRequestFactory()
#         self.view = ListUsersView.as_view()
#         self.url = reverse('list-users')
#
#     @patch('tenant.api_views.Organization.objects.filter')
#     @patch('tenant.api_views.MainUser.objects.filter')
#     def test_list_users(self, mock_main_user_filter, mock_organization_filter):
#         # Mock the organization and users
#         organization = Organization(name="Test Organization 1", organization_id="test_org_id")
#         user1 = MainUser(user_id="user1", organization=organization)
#         user2 = MainUser(user_id="user2", organization=organization)
#         users = [user1, user2]
#
#         # Configure the mocks
#         mock_organization_filter.return_value.first.return_value = organization
#         mock_main_user_filter.return_value.all.return_value = users
#
#         # Make a GET request to the API endpoint
#         request = self.factory.get(self.url)
#         response = self.view(request)
#
#         # Verify the response
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#
# @pytest.mark.django_db
# def test_organization_save(client):
#     organization = Organization(name="Test Organization 2", organization_id="org123")
#     organization.save()
#     assert organization.set_organization_id() == "org123"
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_organization_is_manager(client, mock_setting):
#     organization = Organization(organization_id="org123")
#     setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY = "org123"
#     assert organization.is_manager is True
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_organization_is_not_manager(client, mock_setting):
#     organization = Organization(organization_id="org123")
#     setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY = "otherorg"
#     assert organization.is_manager is False
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_str(client, mock_setting):
#     organization = Organization(name="Test Organization 3", organization_id="org123")
#     main_user = MainUser(user_id="user123", organization=organization)
#     assert str(main_user) == "userID: user123 organization: org123"
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_is_authenticated(client, mock_setting):
#     main_user = MainUser(user_id="user123", organization_id="org123")
#     assert main_user.is_authenticated is True
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_is_not_authenticated(client, mock_setting):
#     main_user = MainUser(user_id="", organization_id="org123")
#     assert main_user.is_authenticated is False
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_is_anonymous(client, mock_setting):
#     main_user = MainUser(user_id="", organization_id="org123")
#     assert main_user.is_anonymous is True
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_is_not_anonymous(client, mock_setting):
#     main_user = MainUser(user_id="user123", organization_id="org123")
#     assert main_user.is_anonymous is False
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_is_staff(client, mock_setting):
#     main_user = MainUser(user_id="user123", organization_id=setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY)
#     assert main_user.is_staff is True
#
#
# @pytest.mark.django_db
# @override_settings(DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}})
# def test_main_user_is_not_staff(client, mock_setting):
#     main_user = MainUser(user_id="user123", organization_id="org123")
#     assert main_user.is_staff is False
