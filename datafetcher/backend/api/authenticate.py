from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from datetime import datetime, timedelta
from loggin.utils import send_to_elasticsearch
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from drf_yasg import openapi
from django.utils import timezone
import json

from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny


class AuthenticateAPIView(APIView):
    """
        API endpoint that allows users to be authenticated.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Authenticate'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            },
            required=['username', 'password'],
        ),
    )
    def post(self, request):
        """
            POST Authenticate the user and generate an access token
        """
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode('utf-8'))
                username = data.get('username')
                password = data.get('password')

                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)

                    token, created = Token.objects.get_or_create(user=user)

                    # If the token was created more than 20 minutes ago, create a new token
                    if not created and token.created < timezone.now() - timedelta(minutes=20):
                        token.delete()
                        token = Token.objects.create(user=user)

                    # Set the token expiry time
                    expiry_time = token.created + timedelta(minutes=20)  # Token expires after 24 hours

                    data_to_send = {
                        'user': username,
                        'auth_timestamp': datetime.now(),
                        'token_expiry': expiry_time.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    send_to_elasticsearch(request=request, index='authentication_history', data=data_to_send)
                    return JsonResponse({'token': "Token "+token.key, 'token_expiry': data_to_send['token_expiry']}, status=200)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format in the request body'}, status=400)
        return JsonResponse({'error': 'Invalid request method'}, status=405)