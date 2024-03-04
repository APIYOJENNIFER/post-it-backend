import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
def test_create_group_api(client):
    """
    Test groups api endpoints 
    :param client
    :return None
    """

    url = reverse("group")
    data = {
        "name":"test group"
    }

    response = client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED