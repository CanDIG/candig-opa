"""
This toy service implements the role of the beacon in this deployment -
accessing the OAuth2/OIDC service for authentication and querying the 
permissions server for authorization.
"""
from typing import Optional
import os

import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

rootCA = os.getenv("ROOT_CA", None)

idp = os.getenv("IDP", "https://oidc:8443/auth/realms/mockrealm/protocol/openid-connect")
client_id = os.getenv("CLIENT_ID", "mock_login_client")
client_secret = os.getenv("CLIENT_SECRET", "mock_login_secret")

permissions_server = os.getenv("PERMISSIONS_SERVER", "http://opa:8181/v1/data/permission")


@app.get("/login")
def get_token(username: Optional[str] = "", password: Optional[str] = ""):
    payload = {'grant_type': 'password',
               'username': username,
               'password': password,
               'redirect_uri': "http://fake_beacon:8000/auth/oidc"}

    if rootCA:
        #response = requests.post(idp, data=payload, auth=(client_id, client_secret), verify=rootCA)
        response = requests.post(f"{idp}/token", data=payload, auth=(client_id, client_secret), verify=False)
    else:
        response = requests.post(f"{idp}/token", data=payload, auth=(client_id, client_secret))

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code)

    try:
        token = response.json()['access_token']
    except:
        raise HTTPException(status_code=500)

    return {"access_token": token}


@app.get("/permissions")
def get_permissions(token: Optional[str] = ""):
    if not token:
        raise HTTPException(status_code=401, detail="Not logged in")

    response = requests.post(permissions_server, 
                             json={"input": {"method": "GET", "path": ["beacon"], "token": token}})
    
    return response.json()