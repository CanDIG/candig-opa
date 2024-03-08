package permissions
#
# This is the set of policy definitions for the permissions engine.
#

default datasets = []

import data.store_token.token as token
access = http.send({"method": "get", "url": "VAULT_URL/v1/opa/access", "headers": {"X-Vault-Token": token}}).body.data.access

paths = http.send({"method": "get", "url": "VAULT_URL/v1/opa/paths", "headers": {"X-Vault-Token": token}}).body.data.paths

get_input_paths = paths.get
post_input_paths = paths.post

#
# Provided:
# input = {
#     'token': user token
#     'method': method requested at data service
#     'path': path to request at data service
# }
#
import data.idp.valid_token
import data.idp.user_key

#
# what controlled access datasets are allowed?
#

default controlled_allowed = []

controlled_allowed = access.controlled_access_list[user_key]{
    valid_token                  # extant, valid token
}

#
# List of all allowed datasets for requests coming from Katsu
#

# allowed datasets
datasets = controlled_allowed
{
    input.body.method = "GET"
    regex.match(get_input_paths[_], input.body.path) == true
}

datasets = controlled_allowed
{
    input.body.method = "POST"
    regex.match(post_input_paths[_], input.body.path) == true
}
