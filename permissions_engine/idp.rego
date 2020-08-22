package idp
# for interacting with the IdP

#
# IdP service configuration
#

env := opa.runtime().env
oidc_base := object.get(env, "IDP", "https://oidc:8443/auth/realms/mockrealm/")
rootCA := object.get(env, "ROOT_CA", "/rootCA.crt")
client_id := object.get(env, "IDP_CLIENT_ID", "mock_permissions_client")
client_secret := object.get(env, "IDP_CLIENT_SECRET", "mockpermissions_secret")

#
# Get IdP endpoints
#
wellknown_url := concat("", [oidc_base, ".well-known/openid-configuration"])
oidc_config := http.send({"method": "get", "url": wellknown_url, "tls_ca_cert_file": rootCA}).body

introspection_url := oidc_config.introspection_endpoint
userinfo_url := oidc_config.userinfo_endpoint

#
# setup basic client authentication for the IdP
#
basic_client_authn := concat(" ", ["Basic", base64.encode(concat(":", [client_id, client_secret]))])

#
# Get the introspection and userinfo data
#
introspect := http.send({"url": introspection_url, "tls_ca_cert_file": rootCA,
                         "headers": {"Authorization": basic_client_authn, "Content-Type": "application/x-www-form-urlencoded"},
                         "method": "post",
                         "raw_body": concat("=", ["token", input.token])}).body

userinfo := http.send({"url": userinfo_url, "tls_ca_cert_file": rootCA,
                       "headers": {"Authorization": concat(" ", ["Bearer", input.token])},
                       "method": "get"}).body