package permissions
#
# This is the set of policy definitions for the permissions engine.
# 

default datasets = []

get_input_paths = array.concat(data.paths.get.katsu, data.paths.get.htsget)
post_input_paths = array.concat(data.paths.post.katsu, data.paths.post.htsget)

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

registered_allowed = data.access.registered_datasets {
    valid_token         # extant, valid token
    trusted_researcher  # has claim we're using for registered access
}

#
# what controlled access datasets are allowed?
#

default controlled_allowed = []

controlled_allowed = data.access.controlled_access_list[email]{
    valid_token                  # extant, valid token
}

#
# List of all allowed datasets for requests coming from Katsu
#

# allowed datasets
datasets = array.concat(array.concat(data.access.open_datasets, registered_allowed), controlled_allowed) 
{
    input.body.method = "GET"
    regex.match(get_input_paths[_], input.body.path) == true
}

datasets = array.concat(array.concat(data.access.open_datasets, registered_allowed), controlled_allowed) 
{
    input.body.method = "POST"
    regex.match(post_input_paths[_], input.body.path) == true
}

# allowed datasets for counting
datasets = array.concat(data.access.open_datasets, data.access.opt_in_datasets) {
    valid_token == true
    input.method = "GET"
    regex.match(get_input_paths[_], input.body.path) == true
    input.query_type = "counts"
}
