"""user views module"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer


class UserSignupAPIView(APIView):
    """Define method(s) for signing up"""
    def post(self, request):
        """a function for signing up a user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSigninAPIView(APIView):
    """Define method(s) for signing in a user"""
    def post(self, request):
        """a function for signing in a user"""
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'error': 'username or password is incorrect'},
                status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key},
            status=status.HTTP_200_OK)
