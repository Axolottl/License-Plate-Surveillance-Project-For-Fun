from rest_framework import permissions
from drf_yasg.views import get_schema_view
from backend.api.backend import BackendAPIView
from backend.api.user import UserAPIView
from backend.api.data import DataAPIView
from backend.api.map import MapDataAPIView
from backend.api.authenticate import AuthenticateAPIView
from backend.api.agent_keys import AgentKeysAPIView
from backend.api.agent import AgentAPIView
from drf_yasg import openapi
from django.conf.urls import url
from django.urls import path

from .views import map_view

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Backend specification for the API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
# MAP
    path('map/', map_view, name='map'),

# API
   # GET fetch a list of the available elements in the API
   path('api/', BackendAPIView.as_view(), name='api'),

# User Authentication
   # POST Authenticate the user and generate an access token
   path('api/authenticate/', AuthenticateAPIView.as_view(), name='authenticate_user'),

# User
   # GET Retrieve the user information , PUT Update the user information, POST Create a new user
   path('api/users/<int:user_id>', UserAPIView.as_view(), name='get_put_post_user_profile'),

# User Data
   # GET Fetch data related to the user , DELETE Delete data related to the
   path('api/users/<int:user_id>/data/<int:data_id>', DataAPIView.as_view(), name='get_delete_platform_data'),
   # GET Fetch all data related to the user
   path('api/users/<int:user_id>/data', DataAPIView.as_view(), name='get_platform_data_no_data_id'),

# @TODO: Add the post process that isn't through REST, RGPC could be the way to go

# Map Data
   # GET Retrieve data for displaying elements on the map
   path('api/map/data/', MapDataAPIView.as_view(), name='get_map_data'),

# Client Agent
   # GET Retrieve information about the client's agent
   path('api/users/<int:user_id>/agents/<int:agent_id>', AgentAPIView.as_view(), name='get_put_client_agent'),
   # GET Retrieve a list of agents associated with the client, POST a new agent to the platform
   path('api/users/<int:user_id>/agents', AgentAPIView.as_view(), name='get_post_client_agent_no_agent_id'),

# Manage Keys
   # GET Retrieve a specific key associated with the client's agent, PUT Update the information of a specific key, DELETE Remove a key from the platform
   path('api/users/<int:user_id>/agents/<int:agent_id>/keys/<int:key_id>', AgentKeysAPIView.as_view(), name='get_put_delete_keys'),
   # GET Retrieve a list of keys associated with the client's agent, POST a new key to the platform
   path('api/users/<int:user_id>/agents/<int:agent_id>/keys', AgentKeysAPIView.as_view(), name='get_post_agent_keys'),

# Swagger documentation
   # GET Retrieve the swagger page that lists all the REST api endpoints
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
]