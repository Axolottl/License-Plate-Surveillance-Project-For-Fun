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
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.models import MapData

from django.shortcuts import render

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

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
        # curl -X 'GET' \
        #    'http://127.0.0.1:8000/api/map/data/?batch_size=1&start_index=1' \
        #    -H 'accept: application/json' \
        #    -H 'X-CSRFToken: myAw33Hqn92zF0uwwTsousm2dgvmo13xU9Xi7UHAM91XQ1ThUetUOyiCLEbmGk3r' \
        #    -H 'Authorization: Token 6cc29b202e71e59885dd72740539435761a47323'
        
        batch_size = request.GET.get('batch_size', 100)  # get the batch size from the query parameters, default to 10
        start_index = request.GET.get('start_index', 1)  # get the start index from the query parameters, default to 1

        map_data = MapData.objects.all().order_by('id')  # get all map data
        paginator = Paginator(map_data, batch_size)  # create a Paginator object

        try:
            map_data_page = paginator.page(start_index)  # get the page of map data
        except (EmptyPage, PageNotAnInteger):
            map_data_page = paginator.page(paginator.num_pages)  # if the page is not valid, return the last page

        map_data_json = serializers.serialize('json', map_data_page.object_list)  # serialize the data to JSON
        map_data_python = json.loads(map_data_json)

        response_data = {
            'current_page': map_data_page.number,
            'total_pages': paginator.num_pages,
            'batch_size': batch_size,
            'start_index': start_index,
            'map_data': map_data_python
        }

        return JsonResponse(f'GET request for map, {response_data}', safe=False)  # return the data as a JSON response


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
    permission_classes = [AllowAny]

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

                    token, created = Token.objects.get_or_create(user=user)

                    data_to_send = {
                        'user': username,
                        'auth_timestamp': datetime.now(),
                    }
                    send_to_elasticsearch(request=request, index='authentication_history', data=data_to_send)
                    return JsonResponse({'token': token.key}, status=200)
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
    permission_classes = [AllowAny]

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



def map_view(request):
    map_data = MapData.objects.all().order_by('id')
    map_data_list = list(map_data.values('id', 'latitude', 'longitude'))  # convert queryset to list of dicts
    return render(request, 'map.html', {'map_data': json.dumps(map_data_list)})  # convert list to JSON