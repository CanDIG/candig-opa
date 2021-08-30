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

def test_user1_gene_by_id_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    for id in ["open1", "open2", "registered3", "controlled4"]:
        response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/genes/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user1_gene_by_id_access_invalid(user1_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/controlled4")
    assert response.status_code == 404

def test_user1_genes_access(user1_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 4
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "registered3" in genes_ids
    assert "controlled4" in genes_ids

def test_user1_genes_invalid(user1_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "registered3" not in genes_ids
    assert "controlled4" not in genes_ids


@pytest.fixture(scope="session")
def user2_token():
    """
    Return the token for user2
    """
    return helper_get_user_token("user2", "pass2")

def test_user2_gene_by_id_access(user2_token):
    """"
    Make sure user1 has access to open1, open2, and controlled5
    """
    for id in ["open1", "open2", "controlled5"]:
        response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/genes/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user2_gene_by_id_access_invalid(user2_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/controlled5")
    assert response.status_code == 404

def test_user2_genes_access(user2_token):
    """"
    Make sure user1 has access to open1, open2, registered3 and controlled 4
    """
    response = helper_get_katsu_response(user2_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "controlled5" in genes_ids

def test_user2_genes_invalid(user2_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user2_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "registered3" not in genes_ids
    assert "controlled5" not in genes_ids


@pytest.fixture(scope="session")
def user3_token():
    """
    Return the token for user3
    """
    return helper_get_user_token("user3", "pass3", OIDC2_URL)

def test_user3_gene_by_id_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    for id in ["open1", "open2", "registered3", "controlled4", "controlled6"]:
        response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/genes/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user3_gene_by_id_access_invalid(user3_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/controlled4")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/controlled6")
    assert response.status_code == 404

def test_user3_genes_access(user3_token):
    """"
    Make sure user3 has access to open1, open2, registered3, controlled4, and controlled6
    """
    response = helper_get_katsu_response(user3_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 5
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "registered3" in genes_ids
    assert "controlled4" in genes_ids
    assert "controlled6" in genes_ids

def test_user3_genes_invalid(user3_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user3_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "registered3" not in genes_ids
    assert "controlled4" not in genes_ids
    assert "controlled6" not in genes_ids


@pytest.fixture(scope="session")
def user4_token():
    """
    Return the token for user4
    """
    return helper_get_user_token("user4", "pass4", OIDC2_URL)

def test_user4_gene_by_id_access(user4_token):
    """"
    Make sure user4 has access to open1, open2, and controlled4
    """
    for id in ["open1", "open2", "controlled5"]:
        response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/genes/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()

def test_user4_gene_by_id_access_invalid(user4_token):
    """"
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open1")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/open2")
    assert response.status_code == 200
    assert "id" in response.json().keys()
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/registered3")
    assert response.status_code == 404
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes/controlled4")
    assert response.status_code == 404

def test_user4_genes_access(user4_token):
    """"
    Make sure user3 has access to open1, open2, and controlled5
    """
    response = helper_get_katsu_response(user4_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 3
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "controlled5" in genes_ids

def test_user4_genes_invalid(user4_token):
    """
    Make sure invalid token will not have access to datasets other than open datasets
    """
    invalid_token = 'A' + user4_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genes")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 2
    genes_ids = set()
    for gene in response_json["results"]:
        genes_ids.add(gene["id"])
    assert "open1" in genes_ids
    assert "open2" in genes_ids
    assert "controlled5" not in genes_ids