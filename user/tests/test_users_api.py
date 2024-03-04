import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_user_signup_api(client):
    """
    Test the user signup and signin APIs
    :param client
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

    user = User.objects.get(username="testuser")
    assert user.username == "testuser"

    #user signin
    url_signin = reverse('signin')
    data_signin = {
        "username":"testuser",
        "password":"123"
    }
    response_signin = client.post(url_signin, data=data_signin, format="json")
    assert response_signin.status_code == 200
