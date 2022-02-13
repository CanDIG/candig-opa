#!/usr/bin/env bash
set -euo pipefail

readonly ADMIN=kcadmin ADMINPWD=admin
# readonly USER1=user1 USER1PWD=pass1
# readonly USER2=user2 USER2PWD=pass2
readonly REALM=mockrealm
readonly CLIENT_LOGIN_ID=mock_login_client
readonly CLIENT_LOGIN_SECRET=mock_login_secret
readonly CLIENT_PERMISSIONS_ID=mock_permissions_client
readonly CLIENT_PERMISSIONS_SECRET=mockpermissions_secret

readonly BASEURL=http://localhost:8080/auth/realms/${REALM}
readonly OPAURL=https://localhost:8181/v1/data/permissions/datasets
readonly SHIMURL=https://localhost:8180/permissions
readonly KATSU_POSTGRES_DB=metadata
readonly KATSU_POSTGRES_USER=admin
readonly KATSU_POSTGRES_PASSWORD=admin

export OIDC1="http://localhost:8080/auth/realms/mockrealm"
export OIDC2="http://localhost:8081/auth/realms/mockrealm"
export OIDC1_OPENCONNECT="http://localhost:8080/auth/realms/mockrealm/protocol/openid-connect"
export OIDC2_OPENCONNECT="http://localhost:8081/auth/realms/mockrealm/protocol/openid-connect"

export ADMIN ADMINPWD
export USER USERPWD
export CLIENT_LOGIN_ID CLIENT_LOGIN_SECRET
export CLIENT_PERMISSIONS_ID CLIENT_PERMISSIONS_SECRET
export REALM
export BASEURL
export KATSU_POSTGRES_DB KATSU_POSTGRES_USER KATSU_POSTGRES_PASSWORD