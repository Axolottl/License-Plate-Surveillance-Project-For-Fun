from django.shortcuts import render
from authentification.models import SignedDataSerializer
from django.shortcuts import redirect
from authentification.models import Material
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from gnupg import GPG
import subprocess
from loggin.utils import send_to_elasticsearch


@api_view(['GET'])
def get_server_public_key(request):
    """
    Return the server public key.
    """

    gpg = GPG()
    public_key = gpg.export_keys("server")
    return Response({"public_key": public_key}, status=200)


@api_view(['POST'])
def receive_initial_public_key(request):
    """
    Receive the initial public key from the user. This is the first step of the registration process.
    """

    if request.method == 'POST':
        serializer = SignedDataSerializer(data=request.data)
        if serializer.is_valid():
            signed_data = serializer.validated_data['signed_data']
            signature = serializer.validated_data['signature']

            gpg = GPG()
            result = gpg.verify_data(signed_data, signature)

            if result.valid:
                try:
                    material = Material.objects.get(public_key=result.public_key)
                    send_data = {
                        'public_key': result.public_key,
                        'message': 'Public key already registered.',
                    }
                    send_to_elasticsearch(request=request, index='registration_agent', data=send_data)
                    return Response({"detail": "Public key already registered."}, status=401)
                except Material.DoesNotExist:
                    material = Material.objects.create(public_key=result.public_key)
                    send_data = {
                        'public_key': result.public_key,
                        'message': 'Public key registered.',
                    }
                    send_to_elasticsearch(request=request, index='registration_agent', data=send_data)
                    return Response({"detail": "Public key registered."})
            else:
                return Response({"detail": "Invalid signature."}, status=401)
        else:
            print(serializer) 
            return Response(serializer.errors, status=300)


@api_view(['POST'])
def verify_signature(request):
    """
    Verify the signature of the user. This is the second step of the registration process.
    """
    
    serializer = SignedDataSerializer(data=request.data)
    if serializer.is_valid():
        signed_data = serializer.validated_data['signed_data']
        signature = serializer.validated_data['signature']

        gpg = GPG()
        result = gpg.verify_data(signed_data, signature)

        if result.valid:
            try:
                material = Material.objects.get(public_key=result.public_key)
                user = authenticate(request, username=material.user.username, password=result.password)
                if user is not None:
                    login(request, user)
                    if 'result' in serializer.validated_data:
                        return redirect('/api/ping')
                    else:
                        return Response({"detail": "Signature is valid, user authenticated."})
                else:
                    return Response({"detail": "Invalid user credentials."}, status=401)
            except Material.DoesNotExist:
                return Response({"detail": "Public key not registered."}, status=401)
        else:
            return Response({"detail": "Invalid signature."}, status=401)
    else:
        return Response(serializer.errors, status=400)