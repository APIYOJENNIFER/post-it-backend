"""Test cases for groups APIs"""
import pytest
from django.urls import reverse
from rest_framework import status
from group.models import Group


@pytest.mark.django_db
def test_group_create(api_client, authenticate_user_with_token):
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
def test_group_list(api_client, authenticate_user_with_token, group_creator):
    """Test GET method for retrieving groups"""
    token = authenticate_user_with_token("testuser", "123",
                                         "testuser@gmail.com")

    Group.objects.create(name="group 1", creator=group_creator)
    Group.objects.create(name="group 2", creator=group_creator)

    url = reverse("group")
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.get(url)

    api_client.credentials()

    assert response.status_code == status.HTTP_200_OK
    expected_size = Group.objects.count()
    assert response.json().get('count') == expected_size


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


@pytest.mark.django_db
def test_group_delete_group_not_found(api_client,
                                      authenticate_user_with_token):
    """Test deletion if group is not existent"""
    token = authenticate_user_with_token("testuser", "123",
                                         "testuser@gmail.com")

    url = reverse("group")
    non_existent_group_id = 0
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.delete(f"{url}{non_existent_group_id}/")

    api_client.credentials()

    assert response.status_code == status.HTTP_404_NOT_FOUND
