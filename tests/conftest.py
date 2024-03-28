"""Reusable test functions"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from group.models import Group


@pytest.fixture(name="api_client")
def fixture_api_client():
    """
    APIClient fixture
    """
    return APIClient()


@pytest.fixture(name="create_user")
def fixture_create_user(db):
    """
    Create a user object
    :param db
    :return None
    """
    def make_user(username, password, email):
        return User.objects.create_user(username=username,
                                        password=password, email=email)
    return make_user


@pytest.fixture
def authenticate_user_with_token(db, api_client, create_user):
    """
    Authenticate user with token after signin
    :params db, api_client, create_user
    """
    def authenticate_user(username, password, email):
        """
        Authenticate user
        """
        if not User.objects.filter(username=username).exists():
            create_user(username, password, email)
        url = reverse('signin')
        data = {
            "username": username,
            "password": password
            }

        response = api_client.post(url, data=data, format="json")
        print(response.data)
        return response.data["token"]
    return authenticate_user


@pytest.fixture(name="group_creator")
def fixture_group_creator(db, create_user):
    """Create a user who is a group creator to test group delete"""

    return create_user(username='test_creator',
                       password='123', email='testcreator@gmail.com')


@pytest.fixture(name="another_user")
def fixture_another_user(db, create_user):
    """Create a user object who isn't a group creator to test group delete"""

    return create_user(username='not_creator',
                       password='123', email='notcreator@gmail.com')


@pytest.fixture
def test_group(db, group_creator):
    """Create a test group"""
    group = Group.objects.create(name="Test group", creator=group_creator)
    group.members.set([group_creator])
    return group
