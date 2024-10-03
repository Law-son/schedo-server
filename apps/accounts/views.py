from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import UserSerializer


@api_view(['POST'])
def signup(request):
    """
    Create a new user account using the provided details.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {'status': 'success', 'message': 'User account created successfully',
             'token': token.key},
            status=status.HTTP_201_CREATED
        )
    else:
        return Response(
            {'status': 'error', 'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


