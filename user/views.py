"""user views module"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer
# Create your views here.


@api_view(['POST'])
def create_user(request):
    """a function for signing up a user"""
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return None


@api_view(['POST'])
def signin_user(request):
    """a function for signing in a user"""
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'error': 'username or password is incorrect'},
                status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)\
            # pylint: disable=no-member
        return Response({
            'token': token.key},
            status=status.HTTP_200_OK)
    return None
