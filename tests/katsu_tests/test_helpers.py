import requests
import os

idp = os.getenv("IDP", "https://oidc1:8443/auth/realms/mockrealm/protocol/openid-connect https://oidc2:8443/auth/realms/mockrealm/protocol/openid-connect").split()
client_id = os.getenv("IDP_CLIENT_ID", "mock_login_client")
client_secret = os.getenv("IDP_CLIENT_SECRET", "mock_login_secret")
idp_map = {
    "oidc1": "http://localhost:8080/auth/realms/mockrealm/protocol/openid-connect",
    "oidc2": "http://localhost:8081/auth/realms/mockrealm/protocol/openid-connect"
}

def helper_get_user_token(username, password, oidc_name="oidc1"):
    oidc = idp_map[oidc_name]
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'redirect_uri': "http://fake_beacon:8000/auth/oidc"}
    response = requests.post(f"{oidc}/token", auth=(client_id, client_secret), data=payload)
    token = response.json()['access_token']
    return token

def helper_get_katsu_response(token, url):
    response = requests.get(url, headers={"X-CANDIG-LOCAL-OIDC":f"\"{token}\""})
    return response