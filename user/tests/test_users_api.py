import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

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

@pytest.mark.django_db
def test_user_signup_api(client):
    """
    Test the user signup API
    :param client
    :return None
    """

    url = reverse('signup')
    data = {
        "username":"testuser",
        "password":"123",
        "email":"testuser@gmail.com"
    }
    response = client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(username="testuser")
    assert user.username == "testuser"

@pytest.mark.django_db
def test_user_signin_api(client, create_user):
    """
    Test the user signin API
    :param client, create_user
    :return None
    """
    create_user("testuser", "123", "testuser@gmail.com")
    url = reverse('signin')
    data = {
        "username":"testuser",
        "password":"123"
    }

    response = client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_200_OK
