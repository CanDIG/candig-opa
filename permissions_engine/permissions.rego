package permissions
#
# This is the set of policy definitions for the permissions engine.
# 

default datasets = []

open_datasets = data.access.open_datasets
registered_datasets = data.access.registered_datasets

controlled_access_list = data.access.controlled_access_list
opt_in_datasets = data.access.opt_in_datasets

input_paths = array.concat(array.concat(data.paths.katsu, data.paths.htsget), data.paths.candigv1)

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
import data.idp.username

#
# is registered access allowed?
# TODO: decide on claim we're using for registered access
#

default registered_allowed = []

registered_allowed = registered_datasets {
    valid_token         # extant, valid token
    trusted_researcher  # has claim we're using for registered access
}

#
# what controlled access datasets are allowed?
#

default controlled_allowed = []

controlled_allowed = controlled_access_list[username]{
    valid_token                  # extant, valid token
}

#
# List of all allowed datasets for requests coming from Katsu
#

# allowed datasets
datasets = array.concat(array.concat(open_datasets, registered_allowed), controlled_allowed) 
{
    input.body.method = "GET"                   # only allow GET requests
    regex.match(input_paths[_], input.body.path) == true
}

# allowed datasets for counting
datasets = array.concat(open_datasets, opt_in_datasets) {
    valid_token == true
    input.method = "GET"
    regex.match(input_paths[_], input.body.path) == true
    input.query_type = "counts"
}
