from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import authenticate

# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data
    first_name = data.get('firstname')
    last_name = data.get('lastname')
    email = data.get('email')
    password = data.get('password')

    print(first_name, last_name, email, password)

    if not email or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=email).exists():
        return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(first_name=first_name, last_name=last_name, username=email, password=password)
    user.save()
    
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    data = request.data
    username = data.get('email')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = request.data.get('token')
    if token is not None:
        try:
            outstanding_token = OutstandingToken.objects.get(token=token)
            BlacklistedToken.objects.create(token=outstanding_token)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except OutstandingToken.DoesNotExist:
            return Response({'detail': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'detail': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)


