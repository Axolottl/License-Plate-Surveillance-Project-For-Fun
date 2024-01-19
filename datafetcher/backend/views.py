from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from loggin.utils import send_to_elasticsearch
from backend.api import get_all_api_endpoints
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
import json

header_param = openapi.Parameter('local',openapi.IN_HEADER,description="local header param", type=openapi.IN_HEADER)

class MapDataAPIView(APIView):
    """
        API endpoint that allows the interactive map to fetch data for displaying elements on the map.
        Optional parameters:
        - batch_size: the number of elements to fetch
        - start_index: the index of the first element to fetch
    """
    @swagger_auto_schema(tags=['MapData'])
    def get(self, request):
        batch_size = request.GET.get('batch_size', 100)
        start_index = request.GET.get('start_index', 1)
        return JsonResponse({'message': f'GET request for map, data {data_id}, batch_size {batch_size}, start_index {start_index}'})

class UserAPIView(APIView):
    """
        API endpoint that allows users to be viewed or edited.
    """
    @swagger_auto_schema(tags=['Users'])
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        profile_data = {
            'username': user.username,
            'email': user.email,
        }
        return JsonResponse(profile_data)

    @swagger_auto_schema(tags=['Users'])
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.username = request.data.get('username', user.username)
        user.email = request.data.get('email', user.email)
        user.save()

        return JsonResponse({'message': 'User profile updated successfully'})

class DatasAPIView(APIView):
    """
        API endpoint that allows datas to be viewed or edited.
    """
    @swagger_auto_schema(tags=['Data'])
    def get(self, request, user_id, data_id=None):
        """
            GET Fetch data related to the user
            Optional parameters:
            - batch_size: the number of elements to fetch
            - start_index: the index of the first element to fetch
        """
        batch_size = request.GET.get('batch_size', 100)
        start_index = request.GET.get('start_index', 1)
        return JsonResponse({'message': f'GET request for user {user_id}, data {data_id}, batch_size {batch_size}, start_index {start_index}'})
        pass

    @swagger_auto_schema(tags=['Data'])
    def delete(self, request, user_id, data_id):
        """
            DELETE Delete data related to the user
        """
        pass

class AgentAPIView(APIView):
    """
        API endpoint that allows agents to be viewed or edited.
    """
    @swagger_auto_schema(tags=['Agent'])
    def get(self, request, user_id, agent_id=None):
        """
            GET Retrieve information about the client's agent
        """
        pass

    @swagger_auto_schema(tags=['Agent'])
    def put(self, request, user_id, agent_id):
        """
            PUT Update information about the client's agent
        """
        pass

    @swagger_auto_schema(tags=['Agent'])
    def post(self, request, user_id):
        """
            POST Create a client's agent
        """
        pass

class AuthenticateAPIView(APIView):
    """
        API endpoint that allows users to be authenticated.
    """
    @swagger_auto_schema(tags=['Authenticate'])
    def post(self, request):
        """
            POST Authenticate the user and generate an access token
        """
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                username = data.get('username')
                password = data.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    access_token = generate_access_token(username)

                    data_to_send = {
                        'user': username,
                        'auth_timestamp': datetime.now(),
                    }
                    send_to_elasticsearch(request=request, index='authentication_history', data=data_to_send)
                    return JsonResponse({'access_token': access_token}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format in the request body'}, status=400)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

class AgentKeysAPIView(APIView):
    """
        API endpoint that allows agents to be viewed or edited.
    """
    @swagger_auto_schema(tags=['AgentKeys'])
    def get(self, request, user_id, agent_id, key_id=None):
        """
            GET Retrieve information about the client's agent
        """
        pass

    @swagger_auto_schema(tags=['AgentKeys'])
    def put(self, request, user_id, agent_id, key_id):
        """
            PUT Update information about the client's agent
        """
        pass
    
    @swagger_auto_schema(tags=['AgentKeys'])
    def delete(self, request, user_id, agent_id, key_id):
        """
            DELETE Delete the client's agent
        """
        pass

    @swagger_auto_schema(tags=['AgentKeys'])
    def post(self, request, user_id, agent_id):
        """
            POST Create the client agent
        """
        pass

class BackendAPIView(APIView):
    """
        API endpoint that allows users to be viewed or edited.
    """
    @api_view(['GET'])
    @csrf_exempt
    @swagger_auto_schema(tags=['API'])
    def api(request):
        api_endpoints = get_all_api_endpoints()
        return Response(api_endpoints, status=200)

    @api_view(['GET'])
    @csrf_exempt
    @swagger_auto_schema(tags=['API'])
    def ping_view(request):
        application_status = check_application_status()

        if application_status:
            status_code = 200
            payload = {'status': 'OK'}
        else:
            status_code = 500
            payload = {'status': 'Error'}

        return Response({"detail": payload}, status_code)