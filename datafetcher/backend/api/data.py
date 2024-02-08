from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
import json
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from backend.models import Data

class DataAPIView(APIView):
    """
        API endpoint that allows data to be viewed or edited.
    """
    @swagger_auto_schema(tags=['Data'])
    def get(self, request, user_id, data_id=None):
        """
            GET Fetch data related to the user
            Optional parameters:
            - batch_size: the number of elements to fetch
            - start_index: the index of the first element to fetch
        """
        batch_size = int(request.GET.get('batch_size', 100))  # get the batch size from the query parameters, default to 10
        start_index = int(request.GET.get('start_index', 1))  # get the start index from the query parameters, default to 1

        if data_id is not None:
            data = Data.objects.filter(id=data_id)
            if data.exists():
                data_json = serializers.serialize('json', data)
                data_python = json.loads(data_json)
                return JsonResponse(data_python, safe=False)
            else:
                return JsonResponse({'error': 'Data not found'}, status=404)
        else:
            data = Data.objects.all().order_by('id')  # get all map data
            paginator = Paginator(data, batch_size)  # create a Paginator object

            try:
                data_page = paginator.page(start_index)  # get the page of map data
            except (EmptyPage, PageNotAnInteger):
                data_page = paginator.page(paginator.num_pages)  # if the page is not valid, return the last page

            map_data_json = serializers.serialize('json', data_page.object_list)  # serialize the data to JSON
            map_data_python = json.loads(map_data_json)

            response_data = {
                'current_page': data_page.number,
                'total_pages': paginator.num_pages,
                'batch_size': batch_size,
                'start_index': start_index,
                'map_data': map_data_python
            }

            return JsonResponse(response_data, safe=False)  # return the data as a JSON response
        
    @swagger_auto_schema(tags=['Data'])
    def delete(self, request, user_id, data_id=None):
        """
            DELETE Delete data related to the user
        """
        if user_id is not None and data_id is not None:
            data = Data.objects.filter(id=data_id)
            if data.exists():
                data.delete()
        elif data_id is None:
            data = Data.objects.filter(user=user_id)
            data.delete()
        return JsonResponse(data={},status=204)