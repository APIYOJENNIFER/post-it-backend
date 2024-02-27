import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_signup_api(client):
    """
    Test the user signup API
    :param api_client
    :return None
    """
    url = reverse('signup')
    payload = {
        "username":"testuser",
        "password":"123",
        "email":"testuser@gmail.com"
    }
    response = client.post(url, data=payload, format="json")
    assert response.status_code == 201
    assert response.data["username"] == payload["username"]