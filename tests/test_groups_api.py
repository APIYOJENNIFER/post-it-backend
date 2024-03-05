"""Test cases for groups APIs"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_create_group_api(api_client, authenticate_user_with_token):
    """
    Test create group api endpoint
    :param client
    :return None
    """

    token = authenticate_user_with_token()

    url = reverse("group")
    data = {
        "name": "test group"
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.post(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_201_CREATED
