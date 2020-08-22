#!/bin/bash
set -euo pipefail

readonly token=${1:-"notoken"}
if [[ "${token}" == "notoken" ]]
then
    >&2 echo "Usage: $0 token"
    exit -1
fi

source config.sh
curl -k "${SHIMURL}" \
    -H "Content-Type: application/json" -H "Accept: application/json" \
    -H "Authorization: Bearer ${token}" \
    -d "{\"method\": \"GET\", \"path\": [\"beacon\"], \"clientSecret\": \"my-secret-root-token\"}"
