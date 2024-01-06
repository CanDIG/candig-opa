#!/usr/bin/env bash

set -Euo pipefail

if [[ -f "/app/initial_setup" ]]; then
    sed -i s/CLIENT_ID/$KEYCLOAK_CLIENT_ID/ /app/permissions_engine/idp.rego && sed -i s/CLIENT_ID/$KEYCLOAK_CLIENT_ID/ /app/permissions_engine/authz.rego
    sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ /app/permissions_engine/idp.rego && sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ /app/permissions_engine/authz.rego

    OPA_SERVICE_TOKEN=$(cat /run/secrets/opa-service-token)
    sed -i s/OPA_SERVICE_TOKEN/$OPA_SERVICE_TOKEN/ /app/permissions_engine/authz.rego

    OPA_ROOT_TOKEN=$(cat /run/secrets/opa-root-token)
    sed -i s/OPA_ROOT_TOKEN/$OPA_ROOT_TOKEN/ /app/permissions_engine/authz.rego
    echo "initializing idp"
    python3 /app/permissions_engine/initialize_idp.py
    rm /app/initial_setup
fi

while [ 0 -eq 0 ]
do
  sleep 60
done
