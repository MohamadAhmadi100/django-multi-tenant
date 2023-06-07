from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class UserRegistrationViewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_user_post(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response['Content-Type'], 'application/json')


class LoginAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
