"""Test cases for users APIs"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


@pytest.mark.django_db
def test_user_signup_api(api_client):
    """
    Test the user signup API
    :param client
    :return None
    """

    url = reverse('signup')
    data = {
        "username": "testuser",
        "password": "123",
        "email": "testuser@gmail.com"
    }
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username="testuser")
    assert user.username == "testuser"


@pytest.mark.django_db
def test_user_signin_api(api_client, create_user):
    """
    Test the user signin API
    :param client, create_user
    :return None
    """
    create_user("testuser", "123", "testuser@gmail.com")
    url = reverse('signin')
    data = {
        "username": "testuser",
        "password": "123"
    }

    response = api_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_200_OK
