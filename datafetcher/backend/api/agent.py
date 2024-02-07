from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from backend.models import AgentData
from backend.serializers import AgentDataSerializer

class AgentAPIView(APIView):
    """
        API endpoint that allows agents to be viewed or edited.
    """
    @swagger_auto_schema(
        tags=['Agent'],
        manual_parameters=[
            openapi.Parameter('batch_size', openapi.IN_QUERY, description="Batch size", type=openapi.TYPE_INTEGER, default=100),
            openapi.Parameter('start_index', openapi.IN_QUERY, description="Start index", type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, user_id, agent_id=None):
        """
            GET Retrieve information about the client's agent
        """
        batch_size = int(request.GET.get('batch_size', 100))  # get the batch size from the query parameters, default to 100
        start_index = int(request.GET.get('start_index', 1))  # get the start index from the query parameters, default to 1

        if agent_id:
            agent_data = AgentData.objects.filter(user_id=user_id, id=agent_id).order_by('id')  # get all agent data for the specified user and agent
        else:
            agent_data = AgentData.objects.filter(user_id=user_id).order_by('id')  # get all agent data for the specified user

        paginator = Paginator(agent_data, batch_size)  # create a Paginator object

        try:
            agent_data_page = paginator.page(start_index)  # get the page of agent data
        except (EmptyPage, PageNotAnInteger):
            agent_data_page = paginator.page(paginator.num_pages)  # if the page is not valid, return the last page

        agent_data_json = serializers.serialize('json', agent_data_page.object_list)  # serialize the data to JSON
        agent_data_python = json.loads(agent_data_json)

        response_data = {
            'current_page': agent_data_page.number,
            'total_pages': paginator.num_pages,
            'batch_size': batch_size,
            'start_index': start_index,
            'agent_data': agent_data_python
        }

        return JsonResponse(response_data, safe=False)  # return the data as a JSON response

    @swagger_auto_schema(tags=['Agent'],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
        ])
    def put(self, request, user_id, agent_id):
        """
            PUT Update information about the client's agent
        """
        agent = AgentData.objects.get(user_id=user_id, id=agent_id)
        agent_serializer = AgentDataSerializer(agent, data=request.data)
        if agent_serializer.is_valid():
            agent_serializer.save()

        agent_data_json = serializers.serialize('json', [agent])  # serialize the data to JSON
        agent_data_python = json.loads(agent_data_json)

        response_data = {
            'agent': agent_data_python
        }

        return JsonResponse(response_data, safe=False)  # return the data as a JSON response

    @swagger_auto_schema(tags=['Agent'],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
        ])
    def post(self, request, user_id):
        """
            POST Create a client's agent
        """
        agent_serializer = AgentDataSerializer(data=request.data)
        if agent_serializer.is_valid():
            agent = agent_serializer.save(user_id=user_id)

        agent_data_json = serializers.serialize('json', [agent])  # serialize the data to JSON
        agent_data_python = json.loads(agent_data_json)

        response_data = {
            'agent': agent_data_python
        }

        return JsonResponse(response_data, safe=False)  # return the data as a JSON response