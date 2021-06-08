import pytest
import requests
import time
"""
This test suite will cover the manual tests in README.md, ensuring that
authorization happens correctly
- beacon permissions
- counts permissions
- registered/controlled access 
- expired token
Plus maybe some others that aren't in there
- modified but live token
"""

BEACON_URL="http://localhost:8000"
LOGIN=f"{BEACON_URL}/login"
PERMISSIONS=f"{BEACON_URL}/permissions"
PERMISSIONS_COUNT=f"{BEACON_URL}/permissions_count"

def helper_get_user_token(username, password):
    token_field = "access_token"

    response = requests.get(f"{LOGIN}?username={username}&password={password}")
    assert response.status_code == 200

    body = response.json()
    assert token_field in body
    return body[token_field]


def helper_get_permissions(token, url):
    response = requests.get(f"{url}?token={token}")
    assert response.status_code == 200

    body = response.json()
    assert "datasets" in body
    return body["datasets"]


@pytest.fixture(scope="session")
def user1_token():
    """
    Return the token for user1
    """
    return helper_get_user_token("user1", "pass1")


def test_user1_controlled_access(user1_token):
    """"
    Make sure user1 has access to controlled4
    """
    datasets = helper_get_permissions(user1_token, PERMISSIONS)
    assert "controlled4" in datasets


def test_user1_registered_access(user1_token):
    """
    User1, being a trusted researcher, should have acess to registered3
    """
    datasets = helper_get_permissions(user1_token, PERMISSIONS)
    assert "registered3" in datasets

def test_user1_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    datasets = helper_get_permissions(invalid_token, PERMISSIONS)
    assert "registered3" not in datasets
    assert "controlled4" not in datasets
    assert "open1" in datasets
    assert "open2" in datasets

def test_user1_opt_in_access(user1_token):
    """
    Make sure user1 has access to opt in dataset controlled4
    """
    datasets = helper_get_permissions(user1_token, PERMISSIONS_COUNT)
    assert "controlled4" in datasets
    assert "open1" in datasets
    assert "open2" in datasets

@pytest.fixture(scope="session")
def user2_token():
    """
    Return the token for user2
    """
    return helper_get_user_token("user2", "pass2")


def test_user2_controlled_access(user2_token):
    """"
    Make sure user2 has access to controlled5
    """
    datasets = helper_get_permissions(user2_token, PERMISSIONS)
    assert "controlled5" in datasets


def test_user2_registered_access(user2_token):
    """
    User2, not being a trusted researcher, should not have acess to registered3
    """
    datasets = helper_get_permissions(user2_token, PERMISSIONS)
    assert "registered3" not in datasets

def test_user2_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    datasets = helper_get_permissions(invalid_token, PERMISSIONS)
    assert "controlled5" not in datasets
    assert "open1" in datasets
    assert "open2" in datasets

def test_user2_opt_in_access(user2_token):
    """
    Make sure user 2 has access to opt in dataset controlled4
    """
    datasets = helper_get_permissions(user2_token, PERMISSIONS_COUNT)
    assert "controlled4" in datasets
    assert "open1" in datasets
    assert "open2" in datasets