from django.urls import get_resolver
import backend.urls as urls
from datafetcher.settings import HOST_NAME
import json

def get_all_api_endpoints():
    """
    Return all the API endpoints.
    """
    urlconf = urls.urlpatterns
    api_endpoints = {}
    for url in urlconf:
        if hasattr(url, 'name') and hasattr(url, 'pattern'):
            # api endpoints append in the format of {name: url}
            api_endpoints[url.name] = HOST_NAME+"/"+str(url.pattern)
    return api_endpoints