#!/usr/bin/env bash
# Start up keycloak and config for new user & client
#
set -euo pipefail

source /opt/jboss/config.sh
readonly KC_PATH=/opt/jboss/keycloak/bin

echo "# Connecting to keycloak..."
${KC_PATH}/kcadm.sh config credentials --server http://localhost:8080/auth --realm master --user ${ADMIN} --password ${ADMINPWD}

echo "# Creating user"
${KC_PATH}/add-user-keycloak.sh -r ${REALM} -u ${USER} -p ${USERPWD}

echo "# Now restart"