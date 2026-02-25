from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

# Create your tests here.
# majority of this code is obtained using AI
User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'

        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
                'password': 'test12345',  # Updated to at least 8 characters
                'password2': 'test12345',
            'phone_number': '0712345678'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(User.objects.count(), 1)

    def test_user_registration_password_mismatch(self):
        data = self.user_data.copy()
        data['password2'] = 'wrongpassword'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        # First create a user
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test12345'  # Updated to match new password
        )

        # Then try to login
        login_data = {
            'email': 'test@example.com',
            'password': 'test12345'  # Updated to match new password
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_password(self):
        User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test12345'  # Updated to match new password
        )

        login_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)