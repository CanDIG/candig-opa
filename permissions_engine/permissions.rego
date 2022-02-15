package permissions
#
# This is the set of policy definitions for the permissions engine.
# 

default datasets = []

open_datasets = ["open1", "open2", "dataset_3", "testdset3"]
registered_datasets = ["registered3"]

controlled_access_list = {"user1": ["controlled4"],    # TODO - should use iss:sub for this rather than username
                          "user2": ["controlled5"],
                          "user3": ["controlled4", "controlled6"],
                          "user4": ["controlled5"],
                          "jimli": ["mock1", "mock2", "1kgenome"]}
opt_in_datasets = ["controlled4"]

input_paths = ["/api/phenopackets/?.*", "/api/datasets/?.*", "/api/diagnoses/?.*", "/api/diseases/?.*",
                 "/api/genes/?.*", "/api/genomicinterpretations/?.*", "/api/htsfiles/?.*", "/api/individuals/?.*",
                 "/api/interpretations/?.*", "/api/metadata/?.*", "/api/phenopackets/?.*", "/api/phenotypicfeatures/?.*",
                 "/api/procedures/?.*", "/api/variants/?.*", "/api/biosamples/?.*", "/api/overview",
                 #mcode data models input paths
                 "/api/mcodepackets/?.*", "/api/medicationstatements/?.*", "/api/cancerrelatedprocedures/?.*",
                 "/api/tnmstaging/?.*", "/api/cancerconditions/?.*", "/api/labsvital/?.*", 
                 "/api/genomicsreports/?.*", "/api/genomicregionsstudied/?.*", "/api/cancergeneticvariants/?.*",
                 "/api/geneticspecimens/?.*"]

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
