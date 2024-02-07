from django.http import JsonResponse
from backend.utils.api import get_all_api_endpoints
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class BackendAPIView(APIView):
    """
        API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(tags=['API'])
    def get(self, request):
        api_endpoints = get_all_api_endpoints()
        return JsonResponse(api_endpoints, status=200)