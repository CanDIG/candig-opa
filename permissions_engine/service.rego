package service
#
# Verifies that a service is who it says it is
#

import data.store_token.token as token

url = concat("/", ["http://vault:8200/v1", input.service, "token", input.token])
service_token = http.send({"method": "get", "url": url, "headers": {"X-Vault-Token": token}}).body.data.token

verified {
    service_token == input.token
}