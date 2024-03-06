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
import data.idp.trusted_researcher
import data.idp.email

#
# is registered access allowed?
# TODO: decide on claim we're using for registered access
#

default registered_allowed = []

registered_allowed = access.registered_datasets {
    valid_token         # extant, valid token
    trusted_researcher  # has claim we're using for registered access
}

#
# what controlled access datasets are allowed?
#

default controlled_allowed = []

controlled_allowed = access.controlled_access_list[email]{
    valid_token                  # extant, valid token
}

#
# List of all allowed datasets for requests coming from Katsu
#

# allowed datasets
datasets = array.concat(array.concat(access.open_datasets, registered_allowed), controlled_allowed)
{
    input.body.method = "GET"
    regex.match(get_input_paths[_], input.body.path) == true
}

datasets = array.concat(array.concat(access.open_datasets, registered_allowed), controlled_allowed)
{
    input.body.method = "POST"
    regex.match(post_input_paths[_], input.body.path) == true
}

# allowed datasets for counting
datasets = array.concat(access.open_datasets, access.opt_in_datasets) {
    valid_token == true
    input.method = "GET"
    regex.match(get_input_paths[_], input.body.path) == true
    input.query_type = "counts"
}
