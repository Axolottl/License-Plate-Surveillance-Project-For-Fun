from elasticsearch import Elasticsearch
from datafetcher.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_PORT
from datetime import datetime
from django.http import JsonResponse

def connect_to_elasticsearch():
    # Connect to Elasticsearch
    elastic_search = Elasticsearch([{'host': ELASTICSEARCH_HOST, 'port': ELASTICSEARCH_PORT}])
    return elastic_search

def send_to_elasticsearch(request ,index ,data):
    # Send data to Elasticsearch for storage
    elastic_search = connect_to_elasticsearch()
    
    # Add timestamp to data
    data.update({
        'timestamp': datetime.now(),
    })

    # Send data to Elasticsearch
    elastic_search.index(index=index, doc_type='_doc', body=data)

    return JsonResponse({'status': 'Data sent to Elasticsearch'})