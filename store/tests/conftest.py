
from django.contrib.auth.models import User
from rest_framework.test import APIClient
import pytest

"""
By using this fixture in a PyTest test case, you can easily make API requests
and test the behavior of your Django application's APIs. The advantage of using 
fixtures is that the setup logic (in this case, creating an instance of APIClient) 
is executed only once per test session, and the returned value is passed as an 
argument to the test function that uses the fixture. This makes the code more readable,
and helps you avoid repeating setup logic in multiple tests.
"""
@pytest.fixture
def api_client():
    return APIClient()


"""
Inner function used 
"""
@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate