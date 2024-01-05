#!/usr/bin/env bash

set -Euo pipefail

OPA_ROOT_TOKEN=$(cat /run/secrets/opa-root-token)

if [[ -f "/app/initial_setup" ]]; then
    sed -i s/CLIENT_ID/$KEYCLOAK_CLIENT_ID/ /app/permissions_engine/idp.rego && sed -i s/CLIENT_ID/$KEYCLOAK_CLIENT_ID/ /app/permissions_engine/authz.rego
    sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ /app/permissions_engine/idp.rego && sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ /app/permissions_engine/authz.rego

    OPA_SERVICE_TOKEN=$(cat /run/secrets/opa-service-token)
    sed -i s/OPA_SERVICE_TOKEN/$OPA_SERVICE_TOKEN/ /app/permissions_engine/authz.rego

    sed -i s/OPA_ROOT_TOKEN/$OPA_ROOT_TOKEN/ /app/permissions_engine/authz.rego

    echo "initializing stores"
    python3 /app/initialize_vault_store.py
    if [[ $? -eq 0 ]]; then
        rm /app/initial_setup
        rm /app/bearer.txt
        echo "!!!!!! SETUP COMPLETE !!!!!!"
    else
        echo "initialization failed, try again"
    fi
fi


while [ 0 -eq 0 ]
do
  echo "storing vault token"
  python3 get_vault_store_token.py
  if [[ $? -eq 0 ]]; then
      echo "vault token stored"
      sleep 300
  else
      echo "vault token not stored"
      sleep 30
  fi
done
