from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
import json
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.models import MapData
from drf_yasg import openapi

class MapDataAPIView(APIView):
    """
        API endpoint that allows the interactive map to fetch data for displaying elements on the map.
        Optional parameters:
        - batch_size: the number of elements to fetch
        - start_index: the index of the first element to fetch
    """
    @swagger_auto_schema(
        tags=['MapData'],
        manual_parameters=[
            openapi.Parameter('batch_size', openapi.IN_QUERY, description="Batch size", type=openapi.TYPE_INTEGER, default=100),
            openapi.Parameter('start_index', openapi.IN_QUERY, description="Start index", type=openapi.TYPE_INTEGER, default=1),
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        
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

        return JsonResponse({'message': 'GET request for map', 'content': response_data}, safe=False)  # return the data as a JSON response
