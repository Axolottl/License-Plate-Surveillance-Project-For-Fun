from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from django.core.exceptions import ObjectDoesNotExist
from backend.serializers import UserSerializer

class UserAPIView(APIView):
    """
        API endpoint that allows users to be viewed or edited.
    """
    @swagger_auto_schema(tags=['Users'],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
        ])
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(tags=['Users'],
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
            openapi.Parameter('username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="mail", type=openapi.TYPE_STRING),
        ])
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            username = request.GET.get('username', user.username)  # get the username from the query parameters, default to the current username
            email = request.GET.get('email', user.email)  # get the email from the query parameters, default to the current email
            data = {'username': username, 'email': email, **request.data}
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User profile updated successfully'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(tags=['Users'],
    manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Access Token (format: 'Token <token>')", type=openapi.TYPE_STRING),
        openapi.Parameter('username', openapi.IN_QUERY, description="username", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('email', openapi.IN_QUERY, description="email", type=openapi.TYPE_STRING, required=True),
    ])
    def post(self, request, user_id=None):
        username = request.GET.get('username')  # get the username from the query parameters
        email = request.GET.get('email')  # get the email from the query parameters
        if username is None or email is None:
            return Response({'error': 'Both username and email are required'}, status=status.HTTP_400_BAD_REQUEST)
        data = {'username': username, 'email': email, **request.data}
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)