#!/usr/bin/env bash
set -euo pipefail

readonly ADMIN=kcadmin ADMINPWD=admin
readonly USER1=user1 USER1PWD=pass1
readonly USER2=user2 USER2PWD=pass2
readonly REALM=mockrealm
readonly CLIENT_LOGIN_ID=mock_login_client
readonly CLIENT_LOGIN_SECRET=mock_login_secret
readonly CLIENT_PERMISSIONS_ID=mock_permissions_client
readonly CLIENT_PERMISSIONS_SECRET=mockpermissions_secret

readonly BASEURL=http://localhost:8080/auth/realms/${REALM}
readonly OPAURL=https://localhost:8181/v1/data/permissions/datasets
export ADMIN ADMINPWD
export USER USERPWD
export CLIENT_LOGIN_ID CLIENT_LOGIN_SECRET
export CLIENT_PERMISSIONS_ID CLIENT_PERMISSIONS_SECRET
export REALM
export BASEURL
