import json
from backend.models import MapData
from django.shortcuts import render

def map_view(request):
    map_data = MapData.objects.all().order_by('id')
    map_data_list = list(map_data.values('id', 'latitude', 'longitude'))  # convert queryset to list of dicts
    return render(request, 'map.html', {'map_data': json.dumps(map_data_list)})  # convert list to JSON