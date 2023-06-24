# from unittest.mock import patch
#
# import factory
# from main.config import setting
# from rest_framework import status
# from rest_framework.test import APIClient, APITestCase
#
# from tenant.models import Organization, MainUser
#
#
# class OrganizationFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Organization
#
#     name = factory.Faker('name')
#     organization_id = factory.Faker('uuid4')
#
#
# class MainUserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = MainUser
#
#     user_id = factory.Faker('uuid4')
#     email = factory.Faker('email')
#     organization = factory.SubFactory(OrganizationFactory)
#     active = True
#
#
# class ListUsersViewTest(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.organization = OrganizationFactory()
#         self.user = MainUserFactory(organization=self.organization)
#
#     def test_list_users(self):
#         response = self.client.get('/api/user/list', {'organization_id': self.organization.organization_id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#
# class RetrieveUserViewTest(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.organization = OrganizationFactory()
#         self.user = MainUserFactory(organization=self.organization)
#
#     def test_retrieve_user(self):
#         auth0_domain = setting.AUTH0_JWKS_URL.split("/")[2]
#         response = self.client.get(f'https://{auth0_domain}/userinfo',
#                                    {'organization_id': self.organization.organization_id, 'user_id': self.user.user_id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['user_id'], str(self.user.user_id))
#
#
# @patch('requests.get')
# class GetUserDetailsFromAuth0Test(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#
#     def test_get_user_details_from_auth0(self, mock_get):
#         # Mocking the response from Auth0
#         class MockResponse:
#             @staticmethod
#             def json():
#                 return {'user': 'details'}
#
#             status_code = 200
#
#         mock_get.return_value = MockResponse()
#         auth0_domain = setting.AUTH0_JWKS_URL.split("/")[2]
#         response = self.client.get(f'https://{auth0_domain}/userinfo',
#                                    HTTP_AUTHORIZATION='Bearer some_access_token')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'user': 'details'})
#
#
# class RetrieveOrganizationViewTest(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.organization = OrganizationFactory()
#
#     def test_retrieve_organization(self):
#         response = self.client.get('/api/organization', {'organization_id': self.organization.organization_id})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['organization_id'], str(self.organization.organization_id))
#
#
# class ListOrganizationsViewTest(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.organizations = OrganizationFactory.create_batch(5)
#
#     def test_list_organizations(self):
#         response = self.client.get('/api/organization/list')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), len(self.organizations))
