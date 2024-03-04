import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_groups_api(client):
    """
    Test groups api endpoints 
    :param client
    :return None
    """

    url = reverse("group")
    data = {
        "name":"test group"
    }

    response_create = client.post(url, data=data, format="json")
    assert response_create.status_code == 201