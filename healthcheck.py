import json
import os
import re
import sys
import uuid
from http import HTTPStatus
from pathlib import Path
import datetime
import requests

keycloak_url = os.environ.get('KEYCLOAK_PUBLIC_URL')

# Read Docker secrets
with open("/run/secrets/client_secret") as f:
    client_secret = f.read().strip()

with open("/run/secrets/password") as f:
    password = f.read().strip()

def get_token(username=None, password=None, client_id=None, client_secret=None):
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "username": username,
        "password": password,
        "scope": "openid",
    }
    response = requests.post(
        f"{keycloak_url}/auth/realms/candig/protocol/openid-connect/token",
        data=payload,
    )
    if response.status_code == 200:
        return response.json()["access_token"]

def perform_healthcheck():
    auth_token = get_token(username="user2", password=password, client_id="local_candig", client_secret=client_secret)
    headers = {"Authorization": f"Bearer {auth_token}"}
    url = os.environ.get('OPA_URL')

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        print("Health check passed!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Health check failed: {e}")
        return False

if __name__ == "__main__":
    health_status = perform_healthcheck()
    if not health_status:
        sys.exit(1)
