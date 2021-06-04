package idp
# for interacting with the IdP

#
# Configuration
#

env := opa.runtime().env
rootCA := object.get(env, "ROOT_CA", "/rootCA.crt")

#
# Define valid keys
#
key_sets := {"https://oidc:8443/auth/realms/mockrealm" : `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv01+/YRAwXaVVC7qYM1uCVZeRqePwOWQ/IJU9z8fFeuTGMREIltMV865DHFA4ZZRxD2hQWri0D3YkMwfe/qrJeEWxCGzI0wFiemE9ezEwh5d6en8oqBg3YahKWRbGquPBTrz0B5quMKzvG0rTWELYiGIrIaUiNRzDE7Z4tFDzB30oM5o/5O5/gm/vwuA08HqpoYb+/Xql6+R3p7xk7ZtvlhdYKxJbRueOAsUmvlvaKS7xDg8Igx0NuBoZxkeURhVF0ZqjPfZlo7mhL0LpgzIOMLye46Cc5bdaU7T+qpI77QNgcR2xgp89wDqEnqLMLWrhOYCM1X6n+sokZyFloyNqQIDAQAB
-----END PUBLIC KEY-----`}

claims := io.jwt.decode(input.token)[1]

#
# Check if the token is valid
#
valid_token = true {
    input.token                          # token exists
    io.jwt.verify_rs256(input.token, key_sets[claims.iss]) == true
    time_now := time.now_ns()/1000000000
    claims.exp > time_now
}

#
# Check trusted_researcher in the token payload
#

trusted_researcher = true {
    valid_token
    claims.trusted_researcher == true        
}

username := claims.preferred_username        # get username from the token payload