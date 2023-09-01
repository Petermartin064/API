from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from user_app.api.serializers import RegistrationSerializer
from user_app import models

@api_view(['POST'])
def Registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            account = serializer.save()
            
            data = {
                'response': 'Registration successful!',
                'username': account.username,
                'email': account.email,
                'token': Token.objects.get(user=account).key
            }
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

