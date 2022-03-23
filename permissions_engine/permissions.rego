package permissions
#
# This is the set of policy definitions for the permissions engine.
# 

default datasets = []

open_datasets = data.access.open_datasets
registered_datasets = data.access.registered_datasets

controlled_access_list = data.access.controlled_access_list
opt_in_datasets = data.access.opt_in_datasets

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
