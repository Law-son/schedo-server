from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from .models import User

@api_view(['POST'])
def signup(request):
    """
    Create a new user account using the provided details.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if email is None or password is None:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email is already in use'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create(
        email=email,
        password=make_password(password)
    )

    return Response(
        {'message': 'User account created successfully'},
        status=status.HTTP_201_CREATED
    )

