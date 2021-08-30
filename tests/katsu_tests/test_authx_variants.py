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

def test_user1_variants_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled4
    """
    response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 4
    variants_ids = list()
    variants_dscps = list()
    for variant in response_json["results"]:
        variants_ids.append(variant["id"])
        variants_dscps.append(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "registered3" in variants_dscps
    assert "controlled4" in variants_dscps
    
    '''
    Make sure user1 has access to open1, open2, registered3 and controlled4 by id
    '''

    for id in variants_ids:
        response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/variants/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()


def test_user1_variants_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    variants_dscps = set()
    for variant in response_json["results"]:
        variants_dscps.add(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "registered3" not in variants_dscps
    assert "controlled4" not in variants_dscps


@pytest.fixture(scope="session")
def user2_token():
    """
    Return the token for user2
    """
    return helper_get_user_token("user2", "pass2")

def test_user2_variants_access(user2_token):
    """"
    Make sure user2 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    variants_ids = list()
    variants_dscps = list()
    for variant in response_json["results"]:
        variants_ids.append(variant["id"])
        variants_dscps.append(variant["hgvsAllele"]["hgvs"])

    """"
    Make sure user2 has access to open1, open2, and controlled5
    """
    for id in variants_ids:
        response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/variants/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user2_variants_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    variants_dscps = set()
    for variant in response_json["results"]:
        variants_dscps.add(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "registered3" not in variants_dscps
    assert "controlled5" not in variants_dscps


@pytest.fixture(scope="session")
def user3_token():
    """
    Return the token for user3
    """
    return helper_get_user_token("user3", "pass3", OIDC2_URL)

def test_user3_variants_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 5
    variants_ids = list()
    variants_dscps = list()
    for variant in response_json["results"]:
        variants_ids.append(variant["id"])
        variants_dscps.append(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "registered3" in variants_dscps
    assert "controlled4" in variants_dscps
    assert "controlled6" in variants_dscps
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6 by id
    """
    for id in variants_ids:
        response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/variants/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user3_variants_invalid(user3_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    variants_dscps = set()
    for variant in response_json["results"]:
        variants_dscps.add(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "registered3" not in variants_dscps
    assert "controlled4" not in variants_dscps
    assert "controlled6" not in variants_dscps


@pytest.fixture(scope="session")
def user4_token():
    """
    Return the token for user4
    """
    return helper_get_user_token("user4", "pass4", OIDC2_URL)


def test_user4_variants_access(user4_token):
    """"
    Make sure user3 has access to open1, open2, and controlled5
    """
    response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    variants_ids = list()
    variants_dscps = list()
    for variant in response_json["results"]:
        variants_ids.append(variant["id"])
        variants_dscps.append(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "controlled5" in variants_dscps
    
    """"
    Make sure user4 has access to open1, open2, and controlled4 by id
    """
    for id in variants_ids:
        response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/variants/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user4_variants_invalid(user4_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/variants")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    variants_dscps = set()
    for variant in response_json["results"]:
        variants_dscps.add(variant["hgvsAllele"]["hgvs"])
    assert "open1" in variants_dscps
    assert "open2" in variants_dscps
    assert "controlled5" not in variants_dscps