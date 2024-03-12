"""Test cases for groups APIs"""
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
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


@pytest.mark.django_db
def test_group_add_members_successful(api_client,
                                      authenticate_user_with_token,
                                      group_creator):
    """
    Test successful addition of new members to a group by the group creator
    """
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")
    group = Group.objects.create(name="group 1", creator=group_creator)
    user_1 = User.objects.create_user("user_1", "123", "user_1@gmail.com")
    user_2 = User.objects.create_user("user_2", "123", "user_2@gmail.com")

    url = reverse("group")
    data = {
        "members": [user_1.id, user_2.id],
        "group_id": group.id
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.patch(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_group_add_members_permission_denied(api_client,
                                             authenticate_user_with_token,
                                             group_creator):
    """
    Test permission denied when adding new members to a group
    """
    token = authenticate_user_with_token("not_creator", "123",
                                         "notcreator@gmail.com")
    group = Group.objects.create(name="group 1", creator=group_creator)
    user_1 = User.objects.create_user("user_1", "123", "user_1@gmail.com")
    user_2 = User.objects.create_user("user_2", "123", "user_2@gmail.com")

    url = reverse("group")
    data = {
        "members": [user_1.id, user_2.id],
        "group_id": group.id
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.patch(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_group_add_members_bad_request(api_client,
                                       authenticate_user_with_token,
                                       group_creator):
    """
    Test for non existent user when adding new members to a group
    """
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")
    group = Group.objects.create(name="group 1", creator=group_creator)
    non_existent_user_id = 0

    url = reverse("group")
    data = {
        "members": [non_existent_user_id],
        "group_id": group.id
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.patch(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_group_add_members_group_not_found(api_client,
                                           authenticate_user_with_token,
                                           group_creator):
    """
    Test group not found when adding new members to a group
    """
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")
    user_1 = User.objects.create_user("user_1", "123", "user_1@gmail.com")

    non_existent_group_id = 0

    url = reverse("group")
    data = {
        "members": [user_1.id],
        "group_id": non_existent_group_id
    }
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.patch(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_group_retrieve_single_group(api_client,
                                     authenticate_user_with_token,
                                     group_creator):
    """Test GET method for retrieving a single group"""
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")

    group = Group.objects.create(name="group 1", creator=group_creator)

    url = reverse("group", kwargs={"group_id": group.id})
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.get(url)

    api_client.credentials()

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_group_successful_delete_user(api_client,
                                      authenticate_user_with_token,
                                      group_creator):
    """Test successful removal of a user(s) from group"""
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")

    group = Group.objects.create(name="group 1", creator=group_creator)
    user = User.objects.create_user("user_to_delete", "123",
                                    "usertodelete@gmail.com")
    group.members.set([user])

    url = reverse("group", kwargs={"user_id": user.id})
    data = {"group_id": group.id}

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.delete(url, data=data, format="json")

    api_client.credentials()

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_group_only_creator_delete_user(api_client,
                                        authenticate_user_with_token,
                                        group_creator):
    """Test that only group creator can remove a user(s) from group"""
    token = authenticate_user_with_token("testuser", "123",
                                         "testuser@gmail.com")

    group = Group.objects.create(name="group 1", creator=group_creator)
    user = User.objects.create_user("user_to_delete", "123",
                                    "usertodelete@gmail.com")
    group.members.set([user])

    url = reverse("group", kwargs={"user_id": user.id})
    data = {"group_id": group.id}

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.delete(url, data=data, format="json")
    error = response.json().get("error")
    assert error == "Only group creator can remove members"

    api_client.credentials()


@pytest.mark.django_db
def test_group_cannot_remove_creator_from_group(api_client,
                                                authenticate_user_with_token,
                                                group_creator):
    """Test that group creator cannot be removed from group"""
    token = authenticate_user_with_token("test_creator", "123",
                                         "testcreator@gmail.com")

    group = Group.objects.create(name="group 1", creator=group_creator)
    group.members.set([group_creator])

    url = reverse("group", kwargs={"user_id": group_creator.id})
    data = {"group_id": group.id}

    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    response = api_client.delete(url, data=data, format="json")
    error = response.json().get("error")
    assert error == "Cannot remove creator from the group"
    assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.credentials()
