#!/usr/bin/env bash

set -Euo pipefail

if [[ -f "initial_setup" ]]; then
    sed -i s/CLIENT_ID/$IDP_CLIENT_ID/ app/permissions_engine/idp.rego && sed -i s/CLIENT_ID/$IDP_CLIENT_ID/ app/permissions_engine/authz.rego
    sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ app/permissions_engine/idp.rego && sed -i s/OPA_SITE_ADMIN_KEY/$OPA_SITE_ADMIN_KEY/ app/permissions_engine/authz.rego
    
    export OPA_SERVICE_TOKEN=$(cat /run/secrets/opa-service-token)
    export OPA_ROOT_TOKEN=$(cat /run/secrets/opa-root-token)
    sed -i s/OPA_SERVICE_TOKEN/$OPA_SERVICE_TOKEN/ app/permissions_engine/authz.rego
    sed -i s/OPA_ROOT_TOKEN/$OPA_ROOT_TOKEN/ app/permissions_engine/authz.rego
    rm initial_setup
fi

while [ 0 -eq 0 ]
do
  sleep 60
done
