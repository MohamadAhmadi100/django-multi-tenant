# from django.test import TestCase
# from tenant.models import Organization, MainUser
# from unittest.mock import MagicMock
#
#
# class OrganizationModelTestCase(TestCase):
#
#     def setUp(self):
#         # Mock the setting to avoid relying on external configurations
#         self.mocked_setting = MagicMock()
#         self.mocked_setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY = "management_org_key"
#
#     def test_organization_save(self):
#         # Create an organization
#         org = Organization.objects.create(name="Test Org")
#
#         # Test set_organization_id method
#         self.assertEqual(org.set_organization_id(), org.organization_id)
#
#     def test_organization_is_manager_property(self):
#         # Create an organization
#         org = Organization.objects.create(name="Manager Org", organization_id="management_org_key")
#
#         # Patch the setting in Organization model
#         Organization.setting = self.mocked_setting
#
#         # Test is_manager property
#         self.assertTrue(org.is_manager)
#
#
# class MainUserModelTestCase(TestCase):
#
#     def setUp(self):
#         # Mock the setting to avoid relying on external configurations
#         self.mocked_setting = MagicMock()
#         self.mocked_setting.AUTH0_MANAGEMENT_ORGANIZATION_KEY = "management_org_key"
#         self.org = Organization.objects.create(name="Test Org")
#
#     def test_main_user_str(self):
#         # Create a MainUser
#         user = MainUser.objects.create(user_id="123", organization=self.org)
#
#         # Test __str__ method
#         self.assertEqual(str(user), f"userID: {user.user_id} organization: {self.org.organization_id}")
#
#     def test_main_user_is_authenticated_property(self):
#         # Create a MainUser
#         user = MainUser.objects.create(user_id="123", organization=self.org)
#
#         # Test is_authenticated property
#         self.assertTrue(user.is_authenticated)
#
#     def test_main_user_is_anonymous_property(self):
#         # Create a MainUser without user_id
#         user = MainUser(user_id=None, organization=None)
#
#         # Test is_anonymous property
#         self.assertTrue(user.is_anonymous)
#
#     def test_main_user_is_staff_property(self):
#         # Create a MainUser
#         user = MainUser.objects.create(user_id="123", organization=self.org)
#
#         # Patch the setting in MainUser model
#         MainUser.setting = self.mocked_setting
#
#         # Test is_staff property
#         user.organization.organization_id = "management_org_key"
#         self.assertTrue(user.is_staff)

# from django.test import TestCase
# from ..models import Organization, MainUser
# from .factories import OrganizationFactory, MainUserFactory
# from unittest.mock import patch
#
#
# class OrganizationModelTest(TestCase):
#
#     def test_is_manager_property(self):
#         # Assuming AUTH0_MANAGEMENT_ORGANIZATION_KEY is set to "manager_org_key" in your settings
#         org = OrganizationFactory(organization_id="manager_org_key")
#         self.assertTrue(org.is_manager)
#
#         org2 = OrganizationFactory(organization_id="not_manager")
#         self.assertFalse(org2.is_manager)
#
#
# class MainUserModelTest(TestCase):
#
#     def setUp(self):
#         self.user = MainUserFactory()
#
#     def test_is_authenticated_property(self):
#         self.assertTrue(self.user.is_authenticated)
#
#     def test_is_anonymous_property(self):
#         with patch.object(MainUser, 'user_id', None):
#             self.assertTrue(self.user.is_anonymous)
#
#     def test_is_staff_property(self):
#         org = OrganizationFactory(organization_id="manager_org_key")
#         staff_user = MainUserFactory(organization=org)
#         self.assertTrue(staff_user.is_staff)
#
#         non_staff_user = MainUserFactory()
#         self.assertFalse(non_staff_user.is_staff)
