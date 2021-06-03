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



default key_sets ={"https://oidc:8443/auth/realms/mockrealm" : `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv01+/YRAwXaVVC7qYM1uCVZeRqePwOWQ/IJU9z8fFeuTGMREIltMV865DHFA4ZZRxD2hQWri0D3YkMwfe/qrJeEWxCGzI0wFiemE9ezEwh5d6en8oqBg3YahKWRbGquPBTrz0B5quMKzvG0rTWELYiGIrIaUiNRzDE7Z4tFDzB30oM5o/5O5/gm/vwuA08HqpoYb+/Xql6+R3p7xk7ZtvlhdYKxJbRueOAsUmvlvaKS7xDg8Igx0NuBoZxkeURhVF0ZqjPfZlo7mhL0LpgzIOMLye46Cc5bdaU7T+qpI77QNgcR2xgp89wDqEnqLMLWrhOYCM1X6n+sokZyFloyNqQIDAQAB
-----END PUBLIC KEY-----`}
output := io.jwt.decode(input.token)            # decode the token
claims := output[1]
#
# Check if the token is valid
#
valid_token {
    input.token                          # token exists
    some x
    io.jwt.verify_rs256(input.token, key_sets[x]) == true
    claims.iss == x
    time_now := time.now_ns()/1000000000
    claims.exp > time_now
}



#
# Check trusted_researcher in the token payload
#
trusted_researcher {
    claims.trusted_researcher == true        
}


username := claims.preferred_username        # get username from the token payload