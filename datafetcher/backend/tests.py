from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from django.contrib.auth.models import User

class APITests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()

    # API
    def test_api_endpoint(self):
        url = reverse('api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ping_view(self):
        url = reverse('ping')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # User Authentication
    def test_authenticate_user(self):
        url = reverse('authenticate_user')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', json.loads(response.content))

    # User Profile
    def test_get_user_profile(self):
        url = reverse('get_user_profile')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        url = reverse('update_user_profile')
        self.client.force_login(self.user)
        data = {'first_name': 'New', 'last_name': 'Name'}
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Platform Data

    # Map Data

    # Client Agent

    # Manage Keys

    # Swagger and Redoc documentation
    def test_swagger_json(self):
        url = reverse('schema-json')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui(self):
        url = reverse('schema-swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_redoc_ui(self):
        url = reverse('schema-redoc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)