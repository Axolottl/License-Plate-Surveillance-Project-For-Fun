from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from backend.models import AgentKeys
from backend.serializers import AgentKeysSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

class AgentKeysAPIView(APIView):
    """
        API endpoint that allows agent keys to be viewed or edited.
    """
    @swagger_auto_schema(tags=['AgentKeys'])
    def get(self, request, user_id, agent_id, key_id=None):
        """
            GET Retrieve information about the client's agent key
        """
        try:
            if key_id:
                agent_key = AgentKeys.objects.get(agent__user_id=user_id, agent_id=agent_id, id=key_id)
            else:
                agent_key = AgentKeys.objects.filter(agent__user_id=user_id, agent_id=agent_id)
            serializer = AgentKeysSerializer(agent_key, many=not key_id)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'Agent key not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=['AgentKeys'])
    def put(self, request, user_id, agent_id, key_id):
        """
            PUT Update information about the client's agent key
        """
        try:
            agent_key = AgentKeys.objects.get(agent__user_id=user_id, agent_id=agent_id, id=key_id)
            serializer = AgentKeysSerializer(agent_key, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Agent key updated successfully'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'Agent key not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=['AgentKeys'])
    def delete(self, request, user_id, agent_id, key_id):
        """
            DELETE Delete the client's agent key
        """
        try:
            agent_key = AgentKeys.objects.get(agent__user_id=user_id, agent_id=agent_id, id=key_id)
            agent_key.delete()
            return Response({'message': 'Agent key deleted successfully'})
        except ObjectDoesNotExist:
            return Response({'error': 'Agent key not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=['AgentKeys'])
    def post(self, request, user_id, agent_id):
        """
            POST Create the client agent key
        """
        serializer = AgentKeysSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(agent_id=agent_id)
            return Response({'message': 'Agent key created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)