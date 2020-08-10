#!/usr/bin/env bash
# Start up keycloak and config for new user & client
#
set -euo pipefail

source /opt/jboss/config.sh

readonly KC_PATH=/opt/jboss/keycloak/bin

echo "# Connecting to keycloak..."
${KC_PATH}/kcadm.sh config credentials --server http://localhost:8080/auth --realm master --user ${ADMIN} --password ${ADMINPWD}

echo "# Creating realm.."
${KC_PATH}/kcadm.sh create realms -s realm=${REALM} -s enabled=true

echo "# Creating login client.."
LOGIN_ID=$(${KC_PATH}/kcadm.sh create clients -r ${REALM} -s clientId=${CLIENT_LOGIN_ID} \
                               -s enabled=true -s 'redirectUris=["*"]' -s directAccessGrantsEnabled=true \
                               -s secret=${CLIENT_LOGIN_SECRET} \
                               -i)


echo "# Login client ID follows..."
echo $LOGIN_ID

echo "# Login client config follows..."
${KC_PATH}/kcadm.sh get clients/${LOGIN_ID}/installation/providers/keycloak-oidc-keycloak-json -r ${REALM}

echo "# Creating permissions client.."
PERMISSIONS_ID=$(${KC_PATH}/kcadm.sh create clients -r ${REALM} -s clientId=${CLIENT_PERMISSIONS_ID} \
                                     -s secret=${CLIENT_PERMISSIONS_SECRET} \
                                     -s enabled=true -s 'redirectUris=["*"]' \
                                     -i)

echo "# Permissions client ID follows..."
echo $PERMISSIONS_ID

echo "# Client config follows..."
${KC_PATH}/kcadm.sh get clients/${PERMISSIONS_ID}/installation/providers/keycloak-oidc-keycloak-json -r ${REALM}