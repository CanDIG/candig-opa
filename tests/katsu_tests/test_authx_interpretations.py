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

def test_user1_interpretation_by_id_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    for id in ["open1", "open2", "registered3", "controlled4"]:
        response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/interpretations/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user1_interpretation_by_id_access_invalid(user1_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/controlled4")
    assert response.status_code == 404

def test_user1_interpretations_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 4
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "registered3" in interpretations_ids
    assert "controlled4" in interpretations_ids

def test_user1_interpretations_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "registered3" not in interpretations_ids
    assert "controlled4" not in interpretations_ids


@pytest.fixture(scope="session")
def user2_token():
    """
    Return the token for user2
    """
    return helper_get_user_token("user2", "pass2")

def test_user2_interpretation_by_id_access(user2_token):
    """"
    Make sure user1 has access to open1, open2, and controlled5
    """
    for id in ["open1", "open2", "controlled5"]:
        response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/interpretations/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user2_interpretation_by_id_access_invalid(user2_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/controlled5")
    assert response.status_code == 404

def test_user2_interpretations_access(user2_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "controlled5" in interpretations_ids

def test_user2_interpretations_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "registered3" not in interpretations_ids
    assert "controlled5" not in interpretations_ids


@pytest.fixture(scope="session")
def user3_token():
    """
    Return the token for user3
    """
    return helper_get_user_token("user3", "pass3", OIDC2_URL)

def test_user3_interpretation_by_id_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    for id in ["open1", "open2", "registered3", "controlled4", "controlled6"]:
        response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/interpretations/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user3_interpretation_by_id_access_invalid(user3_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/controlled4")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/controlled6")
    assert response.status_code == 404

def test_user3_interpretations_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 5
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "registered3" in interpretations_ids
    assert "controlled4" in interpretations_ids
    assert "controlled6" in interpretations_ids

def test_user3_interpretations_invalid(user3_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "registered3" not in interpretations_ids
    assert "controlled4" not in interpretations_ids
    assert "controlled6" not in interpretations_ids


@pytest.fixture(scope="session")
def user4_token():
    """
    Return the token for user4
    """
    return helper_get_user_token("user4", "pass4", OIDC2_URL)

def test_user4_interpretation_by_id_access(user4_token):
    """"
    Make sure user4 has access to open1, open2, and controlled4
    """
    for id in ["open1", "open2", "controlled5"]:
        response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/interpretations/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user4_interpretation_by_id_access_invalid(user4_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations/controlled4")
    assert response.status_code == 404

def test_user4_interpretations_access(user4_token):
    """"
    Make sure user3 has access to open1, open2, and controlled5
    """
    response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "controlled5" in interpretations_ids

def test_user4_interpretations_invalid(user4_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/interpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    interpretations_ids = set()
    for interpretation in response_json["results"]:
        interpretations_ids.add(interpretation["id"])
    assert "open1" in interpretations_ids
    assert "open2" in interpretations_ids
    assert "controlled5" not in interpretations_ids