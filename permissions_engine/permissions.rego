package permissions
#
# This is the set of policy definitions for the permissions engine.
# 

default datasets = []
default key_sets ={"https://oidc:8443/auth/realms/mockrealm" : `-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAv01+/YRAwXaVVC7qYM1uCVZeRqePwOWQ/IJU9z8fFeuTGMREIltMV865DHFA4ZZRxD2hQWri0D3YkMwfe/qrJeEWxCGzI0wFiemE9ezEwh5d6en8oqBg3YahKWRbGquPBTrz0B5quMKzvG0rTWELYiGIrIaUiNRzDE7Z4tFDzB30oM5o/5O5/gm/vwuA08HqpoYb+/Xql6+R3p7xk7ZtvlhdYKxJbRueOAsUmvlvaKS7xDg8Igx0NuBoZxkeURhVF0ZqjPfZlo7mhL0LpgzIOMLye46Cc5bdaU7T+qpI77QNgcR2xgp89wDqEnqLMLWrhOYCM1X6n+sokZyFloyNqQIDAQAB
-----END PUBLIC KEY-----`}

open_datasets = ["open1", "open2"]
registered_datasets = ["registered3"]

controlled_access_list = {"user1": ["controlled4"],    # TODO - should use iss:sub for this rather than username
                          "user2": ["controlled5"]}
opt_in_datasets = ["controlled4"]
#
# Provided: 
# input = {
#     'token': user token (passed to /introspect and /userinfo)
#     'method': method requested on beacon
#     'path': path to request on beacon
# }
#

import data.idp.introspect
import data.idp.userinfo

default valid_token = false

valid_token = true {
    input.token                          # token exists
    some x
    [valid, header, payload] := io.jwt.decode_verify(     # Decode and verify in one-step
        input.token,
        {                                                 # With the supplied constraints:
            "cert": key_sets[x],                                 #   Verify the token with the certificate
            "iss": x,                                 #   Ensure the issuer claim is the expected value
            "time": time.now_ns()/1000000000,
        }
    )
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


#List of all allowed datasets for this request


datasets = array.concat(array.concat(open_datasets, registered_allowed), controlled_allowed) {
    input.method = "GET"                   # only allow GET requestst
    input.path = ["beacon"]
}

datasets = array.concat(open_datasets, opt_in_datasets) {
     valid_token == true
     input.method = "GET"
     input.path = ["counts"]
}
