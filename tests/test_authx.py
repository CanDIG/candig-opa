import pytest
import requests
import time
import os
import json
from capture_token import helper_get_user_token
from lookup_permissions import helper_get_permissions

"""
This test suite will cover the manual tests in README.md, ensuring that
authorization happens correctly
- registered/controlled access
- expired token
Plus maybe some others that aren't in there
- modified but live token
"""

user1 = os.getenv("USER1_ID")
pass1 = os.getenv("USER1_PASS")
user2 = os.getenv("USER2_ID")
pass2 = os.getenv("USER2_PASS")


@pytest.fixture(scope="session")
def user1_token():
    """
    Return the token for user1
    """
    return helper_get_user_token(user1, pass1)


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
    return helper_get_user_token(user2, pass2)


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


if __name__ == "__main__":
    token = helper_get_user_token(user1, pass1)
    result = helper_get_permissions(token)
    print(result)
