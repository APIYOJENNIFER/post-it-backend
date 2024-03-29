"""user urls module"""
from django.urls import path
from .views import UserSignupAPIView, UserSigninAPIView


urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name='signup'),
    path('signin/', UserSigninAPIView.as_view(), name='signin'),
]
