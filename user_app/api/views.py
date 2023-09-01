from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user_app.api.serializers import RegistrationSerializer



@api_view(['POST'])
def Registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
