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

def test_user1_genomicinterpretations_access(user1_token):
    """"
    Make sure user1 has access to all datasets since genomic interpretations are not filtered
    """
    response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/genomicinterpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 6
    genomicinterpretations_ids = list()
    genomicinterpretations_dscps = list()
    for genomicinterpretation in response_json["results"]:
        genomicinterpretations_ids.append(genomicinterpretation["id"])
        genomicinterpretations_dscps.append(genomicinterpretation["extra_properties"]["description"])
    assert "open1" in genomicinterpretations_dscps
    assert "open2" in genomicinterpretations_dscps
    assert "registered3" in genomicinterpretations_dscps
    assert "controlled4" in genomicinterpretations_dscps
    assert "controlled5" in genomicinterpretations_dscps
    assert "controlled6" in genomicinterpretations_dscps
    
    '''
    Make sure user1 has access to all datasets by id since genomic interpretations are not filtered
    '''

    for id in genomicinterpretations_ids:
        response = helper_get_katsu_response(user1_token, f"{KATSU_URL}/api/genomicinterpretations/{id}")
        assert response.status_code == 200
        assert "id" in response.json().keys()


def test_user1_genomicinterpretations_invalid(user1_token):
    """
    Make sure invalid token still has access to all datasets
    """
    invalid_token = 'A' + user1_token[1:]
    response = helper_get_katsu_response(invalid_token, f"{KATSU_URL}/api/genomicinterpretations")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["count"] == 6
    genomicinterpretations_dscps = set()
    for genomicinterpretation in response_json["results"]:
        genomicinterpretations_dscps.add(genomicinterpretation["extra_properties"]["description"])
    assert "open1" in genomicinterpretations_dscps
    assert "open2" in genomicinterpretations_dscps
    assert "registered3" in genomicinterpretations_dscps
    assert "controlled4" in genomicinterpretations_dscps
    assert "controlled5" in genomicinterpretations_dscps
    assert "controlled6" in genomicinterpretations_dscps
