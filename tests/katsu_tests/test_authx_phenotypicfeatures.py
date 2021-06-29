import pytest
import requests
import time

"""
This test suite will cover the manual testsfor KATSU in README.md, ensuring that
authorization happens correctly
- beacon permissions
- registered/controlled access
- modified but live token
"""

BEACON_URL="http://localhost:8000"
LOGIN=f"{BEACON_URL}/login"
KATSU_URL="http://localhost:8001"
OIDC1_URL="https://oidc1:8443/auth/realms/mockrealm/protocol/openid-connect"
OIDC2_URL="https://oidc2:8443/auth/realms/mockrealm/protocol/openid-connect"

def helper_get_user_token(username, password, oidc_url=OIDC1_URL):
    token_field = "access_token"

    response = requests.get(f"{LOGIN}?username={username}&password={password}&oidc={oidc_url}")
    assert response.status_code == 200

    body = response.json()
    assert token_field in body
    return body[token_field]


def helper_get_katsu_response(token, url):
    response = requests.get(url, headers={"X-CANDIG-LOCAL-OIDC":f"\"{token}\""})
    return response

@pytest.fixture(scope="session")
def user1_token():
    """
    Return the token for user1
    """
    return helper_get_user_token("user1", "pass1")

def test_user1_phenotypicfeature_by_id_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    for id in ["open1", "open2", "registered3", "controlled4"]:
        response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/phenotypicfeatures/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user1_phenotypicfeature_by_id_access_invalid(user1_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/controlled4")
    assert response.status_code == 404

def test_user1_phenotypicfeatures_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 4
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "registered3" in phenotypicfeatures_ids
    assert "controlled4" in phenotypicfeatures_ids

def test_user1_phenotypicfeatures_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "registered3" not in phenotypicfeatures_ids
    assert "controlled4" not in phenotypicfeatures_ids


@pytest.fixture(scope="session")
def user2_token():
    """
    Return the token for user2
    """
    return helper_get_user_token("user2", "pass2")

def test_user2_phenotypicfeature_by_id_access(user2_token):
    """"
    Make sure user1 has access to open1, open2, and controlled5
    """
    for id in ["open1", "open2", "controlled5"]:
        response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/phenotypicfeatures/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user2_phenotypicfeature_by_id_access_invalid(user2_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/controlled5")
    assert response.status_code == 404

def test_user2_phenotypicfeatures_access(user2_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "controlled5" in phenotypicfeatures_ids

def test_user2_phenotypicfeatures_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "registered3" not in phenotypicfeatures_ids
    assert "controlled5" not in phenotypicfeatures_ids


@pytest.fixture(scope="session")
def user3_token():
    """
    Return the token for user3
    """
    return helper_get_user_token("user3", "pass3", OIDC2_URL)

def test_user3_phenotypicfeature_by_id_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    for id in ["open1", "open2", "registered3", "controlled4", "controlled6"]:
        response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/phenotypicfeatures/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user3_phenotypicfeature_by_id_access_invalid(user3_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/controlled4")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/controlled6")
    assert response.status_code == 404

def test_user3_phenotypicfeatures_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 5
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "registered3" in phenotypicfeatures_ids
    assert "controlled4" in phenotypicfeatures_ids
    assert "controlled6" in phenotypicfeatures_ids

def test_user3_phenotypicfeatures_invalid(user3_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "registered3" not in phenotypicfeatures_ids
    assert "controlled4" not in phenotypicfeatures_ids
    assert "controlled6" not in phenotypicfeatures_ids


@pytest.fixture(scope="session")
def user4_token():
    """
    Return the token for user4
    """
    return helper_get_user_token("user4", "pass4", OIDC2_URL)

def test_user4_phenotypicfeature_by_id_access(user4_token):
    """"
    Make sure user4 has access to open1, open2, and controlled4
    """
    for id in ["open1", "open2", "controlled5"]:
        response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/phenotypicfeatures/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user4_phenotypicfeature_by_id_access_invalid(user4_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures/controlled4")
    assert response.status_code == 404

def test_user4_phenotypicfeatures_access(user4_token):
    """"
    Make sure user3 has access to open1, open2, and controlled5
    """
    response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "controlled5" in phenotypicfeatures_ids

def test_user4_phenotypicfeatures_invalid(user4_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/phenotypicfeatures")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    phenotypicfeatures_ids = set()
    for phenotypicfeature in response_json["results"]:
        phenotypicfeatures_ids.add(phenotypicfeature["id"])
    assert "open1" in phenotypicfeatures_ids
    assert "open2" in phenotypicfeatures_ids
    assert "controlled5" not in phenotypicfeatures_ids