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

    token = authenticate_user_with_token("testuser", "123",
                                         "testuser@gmail.com")

    url = reverse("group")
    data = {
        "name": "test group"
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.post(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_get_groups_api(api_client, authenticate_user_with_token):
    """Test GET method for retrieving groups"""
    token = authenticate_user_with_token("testuser", "123",
                                         "testuser@gmail.com")

    url = reverse("group")
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.get(url)

    api_client.credentials()

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_group_delete_success(api_client, authenticate_user_with_token,
                              test_group):
    """Test successful group deletion"""
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")

    url = reverse("group")
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.delete(f"{url}{test_group.id}/")

    api_client.credentials()

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_group_delete_permission_denied(api_client,
                                        authenticate_user_with_token,
                                        test_group):
    """Test for permission denied if user is not a group creator"""
    token = authenticate_user_with_token("not_creator", "123",
                                         "notcreator@gmail.com")

    url = reverse("group")
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.delete(f"{url}{test_group.id}/")

    api_client.credentials()

    assert response.status_code == status.HTTP_403_FORBIDDEN
