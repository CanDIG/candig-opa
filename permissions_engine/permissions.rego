package permissions
#
# This is the set of policy definitions for the permissions engine.
# 

default datasets = []

open_datasets = ["open1", "open2"]
registered_datasets = ["registered3"]

controlled_access_list = {"user1": ["controlled4"],    # TODO - should use iss:sub for this rather than username
                          "user2": ["controlled5"],
                          "user3": ["controlled4", "controlled6"],
                          "user4": ["controlled5"]}
opt_in_datasets = ["controlled4"]

input_paths = ["/api/phenopackets/?.*", "/api/datasets/?.*", "/api/diagnoses/?.*", "/api/diseases/?.*",
                 "/api/genes/?.*", "/api/genomicinterpretations/?.*", "/api/htsfiles/?.*", "/api/individuals/?.*",
                 "/api/interpretations/?.*", "/api/metadata/?.*", "/api/phenopackets/?.*", "/api/phenotypicfeatures/?.*",
                 "/api/procedures/?.*", "/api/variants/?.*", "/api/biosamples/?.*", "/api/overview"]

#
# Provided: 
# input = {
#     'token': user token (passed to /introspect and /userinfo)
#     'method': method requested on beacon
#     'path': path to request on beacon
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
    valid_token                  # extant, valid token
    trusted_researcher  # has claim we're using for registered access
}

#
# what controlled access datasets are allowed?
#

default controlled_allowed = []

controlled_allowed = controlled_access_list[username]{
    valid_token                  # extant, valid token
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

#
# List of all allowed datasets for requests coming from Katsu
#

# allowed datasets
datasets = array.concat(array.concat(open_datasets, registered_allowed), controlled_allowed) 
{
    input.body.method = "GET"                   # only allow GET requestst
    regex.match(input_paths[_], input.body.path) == true
}

# allowed datasets for counting
datasets = array.concat(open_datasets, opt_in_datasets) {
    valid_token == true
    input.method = "GET"
    regex.match(input_paths[_], input.body.path) == true
    input.query_type = "counts"
}