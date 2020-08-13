package permissions

# This is the set of policy definitios for the permissions engine.
# 

default datasets = []

open_datasets = ["open1", "open2"]
registered_datasets = ["registered3"]

controlled_access_list = {"user1": ["controlled4"],    # TODO - should use iss:sub for this rather than username
                          "user2": ["controlled5"]}

#
# OIDC service configuration
# 

env := opa.runtime().env
oidc_base := object.get(env, "IDP", "https://oidc:8443/auth/realms/mockrealm/")
rootCA := object.get(env, "ROOT_CA", "/rootCA.crt")
client_id := object.get(env, "CLIENT_ID", "mock_permissions_client")
client_secret := object.get(env, "CLIENT_SECRET", "mockpermissions_secret")


wellknown_url = concat("", [oidc_base, ".well-known/openid-configuration"])
oidc_config := http.send({"method": "get", "url": wellknown_url, "tls_ca_cert_file": rootCA}).body

introspection_url := oidc_config.introspection_endpoint
userinfo_url := oidc_config.userinfo_endpoint

basic_client_authn := concat(" ", ["Basic", base64.encode(concat(":", [client_id, client_secret]))])

#
# Provided: 
# input = {
#     'token': user token (passed to /introspect and /userinfo)
#     'method': method requested on beacon
#     'path': path to request on beacon
# }
#

foo := input

introspect = http.send({"url": introspection_url, "tls_ca_cert_file": rootCA,
                        "headers": {"Authorization": basic_client_authn, "Content-Type": "application/x-www-form-urlencoded"},
                        "method": "post",
                        "raw_body": concat("=", ["token", input.token])}).body

userinfo = http.send({"url": userinfo_url, "tls_ca_cert_file": rootCA,
                      "headers": {"Authorization": concat(" ", ["Bearer", input.token])},
                      "method": "get"}).body

default valid_token = false

valid_token = true {
    input.token                          # token exists
    introspect.active == true            # currently valid
}

#
# is registered access allowed?
# TODO: decide on claim we're using for registered access
#

default registered_allowed = []

registered_allowed = registered_datasets {
    valid_token == true                  # extant, valid token
    userinfo.trusted_researcher == true  # has claim we're using for registered access
}

#
# what controlled access datasets are allowed?
#

default controlled_allowed = []

iss = introspect.iss
sub = introspect.sub 
username = introspect.username

controlled_allowed = controlled_access_list[username]{
    valid_token == true                  # extant, valid token
}

#
# List of all allowed datasets for this request
#

datasets = array.concat(array.concat(open_datasets, registered_allowed), controlled_allowed) {
  input.method = "GET"                   # only allow GET requests
  input.path = ["beacon"]                # only allow queries to beacon endpoint
}