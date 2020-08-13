#!/bin/bash
set -euo pipefail

# credit: https://gist.github.com/fntlnz/cf14feb5a46b2eda428e000157447309

openssl genrsa -des3 -out rootCA.key 4096
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.crt

# generate IdP cert

openssl genrsa -out oidc/tls.key 2048
openssl req -new -sha256 -key oidc/tls.key -subj '/C=CA/ST=Ontario/O=Demo/CN=oidc' -out oidc/tls.csr
openssl x509 -req -in oidc/tls.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out oidc/tls.crt -days 500 -sha256

# generate OPA cert

openssl genrsa -out permissions_engine/tls.key 2048
openssl req -new -sha256 -key permissions_engine/tls.key -subj '/C=CA/ST=Ontario/O=Demo/CN=opa' -out permissions_engine/tls.csr
openssl x509 -req -in permissions_engine/tls.csr -CA rootCA.crt -CAkey rootCA.key -CAcreateserial -out permissions_engine/tls.crt -days 500 -sha256
