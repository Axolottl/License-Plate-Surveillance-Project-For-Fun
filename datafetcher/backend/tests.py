from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from backend.models import Data

class MapDataAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_map_data(self):
        response = self.client.get(reverse('map_data_api'))
        self.assertEqual(response.status_code, 200)

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_user(self):
        response = self.client.get(reverse('user_api', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_put_user(self):
        response = self.client.put(reverse('user_api', kwargs={'user_id': self.user.id}), {'username': 'newusername', 'email': 'newemail@example.com'})
        self.assertEqual(response.status_code, 200)

class DatasAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.data = Data.objects.create(user=self.user)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_data(self):
        response = self.client.get(reverse('datas_api', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_delete_data(self):
        response = self.client.delete(reverse('datas_api', kwargs={'user_id': self.user.id, 'data_id': self.data.id}))
        self.assertEqual(response.status_code, 204)

class AgentAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_agent(self):
        response = self.client.get(reverse('agent_api', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_put_agent(self):
        response = self.client.put(reverse('agent_api', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

class AuthenticateAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_authenticate(self):
        response = self.client.post(reverse('authenticate_api'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)

class AgentKeysAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_agent_keys(self):
        response = self.client.get(reverse('agent_keys_api', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_put_agent_keys(self):
        response = self.client.put(reverse('agent_keys_api', kwargs={'user_id': self.user.id}))
        self.assertEqual(response.status_code, 200)

class BackendAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_backend(self):
        response = self.client.get(reverse('backend_api'))
        self.assertEqual(response.status_code, 200)

class UserRegistrationAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_user_registration(self):
        response = self.client.post(reverse('user_registration_api'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserLoginAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_user_login(self):
        response = self.client.post(reverse('user_login_api'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserLogoutAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_post_user_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('user_logout_api'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SwaggerAPITestCase(TestCase):
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