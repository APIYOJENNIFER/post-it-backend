import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    """
    Create a user object
    :param db
    :return None
    """
    def make_user(username, password, email):
        User.objects.create_user(username=username, password=password, email=email)
    return make_user

@pytest.fixture
def authenticate_user_with_token(db, api_client, create_user):
    def authenticate_user():
        create_user("testuser", "123", "testuser@gmail.com")
        url = reverse('signin')
        data = {
            "username":"testuser",
            "password":"123"
            }

        response = api_client.post(url, data=data, format="json")
        return response.data["token"]
    return authenticate_user
