from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView

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