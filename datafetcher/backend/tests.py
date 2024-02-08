from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from backend.models import Data
from backend.models import AgentKeys
from backend.models import AgentData
from backend.models import MapData
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from backend.models import Data
import json


class MapDataAPIViewTestCase(APITestCase):
    def setUp(self):
        self.map_data = [MapData.objects.create(latitude=i, longitude=i+1) for i in range(200)]
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def test_get(self):
        response = self.client.get(reverse('get_map_data'), {'batch_size': 50, 'start_index': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(int(response_content['content']['current_page']), 2)
        self.assertEqual(int(response_content['content']['total_pages']), 4)
        self.assertEqual(int(response_content['content']['batch_size']), 50)
        self.assertEqual(int(response_content['content']['start_index']), 2)
        self.assertEqual(len(response_content['content']['map_data']), 50)
        self.assertEqual(response_content['content']['map_data'][0]['fields']['latitude'], 50.0)

# class UserAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
#         self.client.login(username='testuser', password='testpass')

#     def test_get(self):
#         response = self.client.get(reverse('get_put_post_user_profile', kwargs={'user_id': self.user.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'username': 'testuser', 'email': 'testuser@example.com'})

#     def test_put(self):
#         response = self.client.put(reverse('get_put_post_user_profile', kwargs={'user_id': self.user.id}), {'username': 'newuser', 'email': 'newuser@example.com'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'message': 'User profile updated successfully'})
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.username, 'newuser')
#         self.assertEqual(self.user.email, 'newuser@example.com')

#     def test_post(self):
#         response = self.client.post(reverse('get_put_post_user_profile'), {'username': 'newuser', 'email': 'newuser@example.com'})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, {'message': 'User created successfully'})
#         self.assertTrue(User.objects.filter(username='newuser', email='newuser@example.com').exists())

# class DataAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.data = [Data.objects.create(name=f'test{i}') for i in range(200)]

#     def test_get(self):
#         response = self.client.get(reverse('data-list'), {'batch_size': 50, 'start_index': 2})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['current_page'], 2)
#         self.assertEqual(response.data['total_pages'], 4)
#         self.assertEqual(response.data['batch_size'], 50)
#         self.assertEqual(response.data['start_index'], 2)
#         self.assertEqual(len(response.data['map_data']), 50)
#         self.assertEqual(response.data['map_data'][0]['fields']['name'], 'test50')

#     def test_delete(self):
#         response = self.client.delete(reverse('data-detail', kwargs={'data_id': self.data[0].id}))
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Data.objects.filter(id=self.data[0].id).exists())

# class AgentAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.agent_data = [AgentData.objects.create(agent=f'test{i}') for i in range(200)]

#     def test_get(self):
#         response = self.client.get(reverse('get_post_client_agent_no_agent_id'), {'batch_size': 50, 'start_index': 2})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['current_page'], 2)
#         self.assertEqual(response.data['total_pages'], 4)
#         self.assertEqual(response.data['batch_size'], 50)
#         self.assertEqual(response.data['start_index'], 2)
#         self.assertEqual(len(response.data['agent_data']), 50)
#         self.assertEqual(response.data['agent_data'][0]['fields']['name'], 'test50')

#     def test_put(self):
#         response = self.client.put(reverse('get_put_client_agent', kwargs={'agent_id': self.agent_data[0].id}), {'name': 'newname'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['agent'][0]['fields']['name'], 'newname')

#     def test_post(self):
#         response = self.client.post(reverse('agent-list'), {'name': 'newagent'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['agent'][0]['fields']['name'], 'newagent')

# class AuthenticateAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(username='testuser', password='12345')

#     def test_post_authenticate(self):
#         response = self.client.post(reverse('authenticate_api'), {'username': 'testuser', 'password': '12345'})
#         self.assertEqual(response.status_code, 200)

# class AgentKeysAPIViewTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser', password='testpass')
#         self.agent_key = AgentKeys.objects.create(agent="test", key='testkey')
#         self.client.login(username='testuser', password='testpass')

#     def test_get(self):
#         response = self.client.get(reverse('agentkeys-detail', kwargs={'user_id': self.user.id, 'agent_id': self.agent.id, 'key_id': self.agent_key.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'key': 'testkey'})

#     def test_put(self):
#         response = self.client.put(reverse('agentkeys-detail', kwargs={'user_id': self.user.id, 'agent_id': self.agent.id, 'key_id': self.agent_key.id}), {'key': 'newkey'})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'message': 'Agent key updated successfully'})
#         self.agent_key.refresh_from_db()
#         self.assertEqual(self.agent_key.key, 'newkey')

#     def test_delete(self):
#         response = self.client.delete(reverse('agentkeys-detail', kwargs={'user_id': self.user.id, 'agent_id': self.agent.id, 'key_id': self.agent_key.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'message': 'Agent key deleted successfully'})
#         with self.assertRaises(AgentKeys.DoesNotExist):
#             self.agent_key.refresh_from_db()

#     def test_post(self):
#         response = self.client.post(reverse('agentkeys-list', kwargs={'user_id': self.user.id, 'agent_id': self.agent.id}), {'key': 'newkey'})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data, {'message': 'Agent key created successfully'})
#         self.assertTrue(AgentKeys.objects.filter(agent=self.agent, key='newkey').exists())

class BackendAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_backend(self):
        response = self.client.get(reverse('api'))
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response_content['message'], 'GET request for backend')

class SwaggerAPITestCase(TestCase):
    # Swagger documentation tests
    def test_swagger_ui(self):
        url = reverse('schema_swagger_ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)