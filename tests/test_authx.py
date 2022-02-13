import pytest
import requests
import time
import os
import json

"""
This test suite will cover the manual tests in README.md, ensuring that
authorization happens correctly
- registered/controlled access
- expired token
Plus maybe some others that aren't in there
- modified but live token
"""

OIDC1_URL="http://localhost:8080/auth/realms/mockrealm/protocol/openid-connect"
OIDC2_URL="http://localhost:8081/auth/realms/mockrealm/protocol/openid-connect"


def helper_get_user_token(username, password, oidc_url=OIDC1_URL):
    client_id = os.getenv("IDP_CLIENT_ID", "mock_login_client")
    client_secret = os.getenv("IDP_CLIENT_SECRET", "mock_login_secret")

    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'redirect_uri': "http://fake_beacon:8000/auth/oidc"}

    response = requests.post(f"{oidc_url}/token", auth=(client_id, client_secret), data=payload)
    token = response.json()['access_token']
    return token


def helper_get_permissions(token):
    opa_url = os.getenv("OPAURL", "https://localhost:8181/v1/data/permissions/datasets")

    payload = {
                'input': {
                  'headers': {'X-Candig-Local-Oidc': token},
                  'body': {'method': 'GET', 'path': '/api/phenopackets'}
                }
              }

    headers = {
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer my-secret-root-token'
              }

    # NOTE!  Can't verify https using the certificate because from here 'outside' the
    # docker network, the hostname of 'opa' is 'localhost'.  You could fix this by
    # updating /etc/hosts etc.
    response = requests.post(opa_url, headers=headers, data=json.dumps(payload), verify=False)

    assert response.status_code == 200

    body = response.json()
    assert "result" in body
    return body["result"]


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
    datasets = helper_get_permissions(user1_token)
    assert "controlled4" in datasets


def test_user1_registered_access(user1_token):
    """
    User1, being a trusted researcher, should have acess to registered3
    """
    datasets = helper_get_permissions(user1_token)
    assert "registered3" in datasets

def test_user1_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    datasets = helper_get_permissions(invalid_token)
    assert "registered3" not in datasets
    assert "controlled4" not in datasets
    assert "open1" in datasets
    assert "open2" in datasets

def test_user1_opt_in_access(user1_token):
    """
    Make sure user1 has access to opt in dataset controlled4
    """
    datasets = helper_get_permissions(user1_token)
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
    datasets = helper_get_permissions(user2_token)
    assert "controlled5" in datasets


def test_user2_registered_access(user2_token):
    """
    User2, not being a trusted researcher, should not have acess to registered3
    """
    datasets = helper_get_permissions(user2_token)
    assert "registered3" not in datasets

def test_user2_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    datasets = helper_get_permissions(invalid_token)
    assert "controlled5" not in datasets
    assert "open1" in datasets
    assert "open2" in datasets

def test_user2_opt_in_access(user2_token):
    """
    Make sure user 2 has access to opt in dataset controlled5
    """
    datasets = helper_get_permissions(user2_token)
    assert "controlled5" in datasets
    assert "open1" in datasets
    assert "open2" in datasets

@pytest.fixture(scope="session")
def user3_token():
    """
    Return the token for user3
    """
    return helper_get_user_token("user3", "pass3", OIDC2_URL)


def test_user3_controlled_access(user3_token):
    """"
    Make sure user3 has access to controlled4 and controlled6
    """
    datasets = helper_get_permissions(user3_token)
    assert "controlled4" in datasets
    assert "controlled6" in datasets


def test_user3_registered_access(user3_token):
    """
    User3, being a trusted researcher, should have acess to registered3
    """
    datasets = helper_get_permissions(user3_token)
    assert "registered3" in datasets

def test_user3_invalid(user3_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    datasets = helper_get_permissions(invalid_token)
    assert "controlled4" not in datasets
    assert "controlled6" not in datasets
    assert "registered3" not in datasets
    assert "open1" in datasets
    assert "open2" in datasets

def test_user3_opt_in_access(user3_token):
    """
    Make sure user3 has access to opt in dataset controlled4
    """
    datasets = helper_get_permissions(user3_token)
    assert "controlled4" in datasets
    assert "open1" in datasets
    assert "open2" in datasets


@pytest.fixture(scope="session")
def user4_token():
    """
    Return the token for user4
    """
    return helper_get_user_token("user4", "pass4", OIDC2_URL)


def test_user4_controlled_access(user4_token):
    """"
    Make sure user4 has access to controlled6 and controlled5
    """
    datasets = helper_get_permissions(user4_token)
    assert "controlled5" in datasets


def test_user4_registered_access(user4_token):
    """
    User4, not being a trusted researcher, should have acess to registered3
    """
    datasets = helper_get_permissions(user4_token)
    assert "registered3" not in datasets

def test_user4_invalid(user4_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    datasets = helper_get_permissions(invalid_token)
    assert "controlled5" not in datasets
    assert "open1" in datasets
    assert "open2" in datasets

def test_user4_opt_in_access(user4_token):
    """
    Make sure user4 has access to opt in dataset controlled4
    """
    datasets = helper_get_permissions(user4_token)
    assert "controlled5" in datasets
    assert "open1" in datasets
    assert "open2" in datasets


if __name__ == "__main__":
    token = helper_get_user_token("user1", "pass1")
    result = helper_get_permissions(token)
    print(result)