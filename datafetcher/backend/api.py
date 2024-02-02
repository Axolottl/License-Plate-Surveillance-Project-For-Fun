import backend.urls as urls
from datafetcher.settings import HOST_NAME

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