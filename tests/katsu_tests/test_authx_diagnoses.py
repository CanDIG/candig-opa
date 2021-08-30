from test_helpers import helper_get_katsu_response
from test_helpers import helper_get_user_token
import pytest

"""
This test suite will cover the manual testsfor KATSU in README.md, ensuring that
authorization happens correctly
- beacon permissions
- registered/controlled access
- modified but live token
"""

KATSU_URL="http://localhost:8001"
OIDC1_NAME="oidc1"
OIDC2_NAME="oidc2"

@pytest.fixture(scope="session")
def user1_token():
    """
    Return the token for user1
    """
    return helper_get_user_token("user1", "pass1") 

def test_user1_diagnoses_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled4
    """
    response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 4
    diagnoses_ids = list()
    diagnoses_dscps = list()
    for diagnosis in response_json["results"]:
        diagnoses_ids.append(diagnosis["id"])
        diagnoses_dscps.append(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "registered3" in diagnoses_dscps
    assert "controlled4" in diagnoses_dscps
    
    '''
    Make sure user1 has access to open1, open2, registered3 and controlled4 by id
    '''

    for id in diagnoses_ids:
        response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/diagnoses/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()


def test_user1_diagnoses_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    diagnoses_dscps = set()
    for diagnosis in response_json["results"]:
        diagnoses_dscps.add(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "registered3" not in diagnoses_dscps
    assert "controlled4" not in diagnoses_dscps


@pytest.fixture(scope="session")
def user2_token():
    """
    Return the token for user2
    """
    return helper_get_user_token("user2", "pass2")

def test_user2_diagnoses_access(user2_token):
    """"
    Make sure user2 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    diagnoses_ids = list()
    diagnoses_dscps = list()
    for diagnosis in response_json["results"]:
        diagnoses_ids.append(diagnosis["id"])
        diagnoses_dscps.append(diagnosis["extra_properties"]["description"])

    """"
    Make sure user2 has access to open1, open2, and controlled5
    """
    for id in diagnoses_ids:
        response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/diagnoses/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user2_diagnoses_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    diagnoses_dscps = set()
    for diagnosis in response_json["results"]:
        diagnoses_dscps.add(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "registered3" not in diagnoses_dscps
    assert "controlled5" not in diagnoses_dscps


@pytest.fixture(scope="session")
def user3_token():
    """
    Return the token for user3
    """
    return helper_get_user_token("user3", "pass3", OIDC2_URL)

def test_user3_diagnoses_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 5
    diagnoses_ids = list()
    diagnoses_dscps = list()
    for diagnosis in response_json["results"]:
        diagnoses_ids.append(diagnosis["id"])
        diagnoses_dscps.append(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "registered3" in diagnoses_dscps
    assert "controlled4" in diagnoses_dscps
    assert "controlled6" in diagnoses_dscps
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6 by id
    """
    for id in diagnoses_ids:
        response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/diagnoses/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user3_diagnoses_invalid(user3_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    diagnoses_dscps = set()
    for diagnosis in response_json["results"]:
        diagnoses_dscps.add(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "registered3" not in diagnoses_dscps
    assert "controlled4" not in diagnoses_dscps
    assert "controlled6" not in diagnoses_dscps


@pytest.fixture(scope="session")
def user4_token():
    """
    Return the token for user4
    """
    return helper_get_user_token("user4", "pass4", OIDC2_URL)


def test_user4_diagnoses_access(user4_token):
    """"
    Make sure user3 has access to open1, open2, and controlled5
    """
    response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    diagnoses_ids = list()
    diagnoses_dscps = list()
    for diagnosis in response_json["results"]:
        diagnoses_ids.append(diagnosis["id"])
        diagnoses_dscps.append(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "controlled5" in diagnoses_dscps
    
    """"
    Make sure user4 has access to open1, open2, and controlled4 by id
    """
    for id in diagnoses_ids:
        response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/diagnoses/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user4_diagnoses_invalid(user4_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/diagnoses")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    diagnoses_dscps = set()
    for diagnosis in response_json["results"]:
        diagnoses_dscps.add(diagnosis["extra_properties"]["description"])
    assert "open1" in diagnoses_dscps
    assert "open2" in diagnoses_dscps
    assert "controlled5" not in diagnoses_dscps