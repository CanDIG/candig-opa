import requests
import io
import os

KATSU_URL = os.getenv("KATSU_URL")


def post_data(url, data):
    response = requests.post(url, json=data)
    print(response.json())
    return response.json()


def get_project_id(project_title):
    '''
    does a post request to /api/projects
    creates a project with the project title passed in
    returns the project id
    '''
    projects = requests.get(f"{KATSU_URL}/api/projects").json()["results"]
    for project in projects:
        if project["title"] == project_title:
            return project["identifier"]
    result = post_data(f"{KATSU_URL}/api/projects", {"title": project_title, "description": "Project for tests"})
    return result["identifier"]


def get_dataset_id(dataset_title, project_id):
    '''
    does a post request to /api/dataset
    creates a dataset with the dataset title passed in under the project with the project id passed in
    returns the dataset id
    '''
    datasets = requests.get(f"{KATSU_URL}/api/projects/{project_id}").json()["datasets"]
    for dataset in datasets:
        if dataset["title"] == dataset_title:
            return dataset["identifier"]
    dataset = {
        "title": "DATASET_TITLE",
        "data_use": {
            "consent_code": {
                "primary_category": {
                    "code": "GRU"
                },
                "secondary_categories": [
                    {
                        "code": "GSO"
                    }
                ]
            },
            "data_use_requirements": [
                {
                    "code": "COL"
                },
                {
                    "code": "PUB"
                }
            ]
        },
        "project": "PROJECT_ID"
    }
    dataset["title"] = dataset_title
    dataset["project"] = project_id
    return post_data(f"{KATSU_URL}/api/datasets", dataset)["identifier"]


def create_table_ownership(table_id, dataset_id):
    '''
    does a post request to /api/table_ownership
    creates a table ownership between the table with the table id passed in and the dataset with the dataset id passed in
    '''
    table_ownership = {
        "table_id": "TABLE_ID",
        "service_id": "service",
        "dataset": "DATASET_ID"
    }
    table_ownership["table_id"] = table_id
    table_ownership["dataset"] = dataset_id
    post_data(f"{KATSU_URL}/api/table_ownership", table_ownership)


def create_table(table_id):
    '''
    does a post request to /api/tables
    creates a table with the table id passed in
    '''
    table = {
        "ownership_record": "TABLE_ID",
        "name": f"table{table_id}",
        "data_type": "phenopacket"
    }
    table["ownership_record"] = table_id
    post_data(f"{KATSU_URL}/api/tables", table)


def get_meta_data_id():
    '''
    does a post request to /api/metadata
    creates a metadata object
    '''
    return post_data(f"{KATSU_URL}/api/metadata", {"created_by": "test"})["id"]


def create_htsfile(dataset_name, htsfile_description):
    '''
    does post request to /api/htsfiles
    creates a htsfile with the description passed in and with the uri http://{dataset_name}.com under the dataset with the dataset name passed in
    '''
    htsfile = {
        "uri": "http://link.com",
        "hts_format": "UNKNOWN",
        "genome_assembly": "genome_assembly",
        "description": "HTSFILE_ID"
    }
    htsfile["description"] = htsfile_description
    htsfile["uri"] = f"http://{dataset_name}.com"
    post_data(f"{KATSU_URL}/api/htsfiles", htsfile)


def get_biosample(biosample_id, procedure_code_id):
    '''
    returns a sample biosample json with the biosample id passed in
    the biosample object has procedure and sampled tissue field, 
    so the procedure_code_id is used to fill in required fields in procedure and sampled tissue field
    '''
    biosample = {
        "id": "BIOSAMPLE_ID",
        "procedure": {
            "code": {
                "id": "BIOSAMPLE_ID",
                "label": "procedure"
            }
        },
        "sampled_tissue": {
            "id": "BIOSAMPLE_ID",
            "label": "label"
        }
    }
    biosample["id"] = biosample_id
    biosample["procedure"]["code"]["id"] = procedure_code_id
    biosample["sampled_tissue"]["id"] = biosample_id
    return biosample


def get_disease(disease_term_id):
    '''
    returns a sample disease json
    disease_term_id is used for the field required in disease object under term field
    '''
    disease = {
        "term": {
            "id": "DISEASE_ID",
            "label": "label"
        }
    }
    disease["term"]["id"] = disease_term_id
    return disease


def get_gene(gene_id):
    '''
    returns a sample gene json with the gene id passed in
    '''
    gene = {
        "id": "GENE_ID",
        "symbol": "symbol"
    }
    gene["id"] = gene_id
    return gene


def get_variant(variant_allele_hgvs):
    '''
    returns a sample variant json with hgvsAllele type and variant_allele_hgvs for its required field under allele[“hgvs”]
    '''
    variant = {
        "allele_type": "hgvsAllele",
        "allele": {
            "hgvs": "variant for phenopacket with id PHENOPACKET_ID"
        }
    }
    variant["allele"]["hgvs"] = variant_allele_hgvs
    return variant


def get_genomic_interpretation(extra_properties_description, gene_id, variant_id):
    '''
    returns a sample genomic interpretation json with extra_properties description as passed in 
    and related to gene and variant with the id passed in
    '''
    genomic_interpretation = {
        "status": "UNKNOWN",
        "gene": "GENE_ID",
        "variant": "VARIANT_ID",
        "extra_properties": {
            "description": "PHENOPACKET_ID"
        }
    }
    genomic_interpretation["gene"] = gene_id
    genomic_interpretation["variant"] = variant_id
    genomic_interpretation["extra_properties"]["description"] = extra_properties_description
    return genomic_interpretation


def get_diagnosis(extra_properties_description, disease_id, genomic_interpretation_id):
    '''
    returns a sample diagnosis interpretation json with extra_properties description as passed in and related to disease 
    and genomic interpretation with the id passed in
    '''
    diagnosis = {
        "disease": 0,
        "genomic_interpretations": [
            "GENOMICINTERPRETATION_ID"
        ],
        "extra_properties": {
            "description": "PHENOPACKET_ID"
        }
    }
    diagnosis["disease"] = disease_id
    diagnosis["genomic_interpretations"][0] = genomic_interpretation_id
    diagnosis["extra_properties"]["description"] = extra_properties_description
    return diagnosis


def get_phenotypicfeature(type_id, phenopacket_id, biosample_id):
    '''
    returns a sample phenotypic feature json
    phenotypic feature json contains a field with type with the type_id as its id field
    the phenotypic feature is related to the phenopacket with the phenopacket id passed in and the biosample with the biosample id passed in
    '''
    phenotypicfeature = {
        "type": {
            "id": "PHENOTYPICFEATURE_ID",
            "label": "phenotypicfeature label"
        },
        "phenopacket": "PHENOPACKET_ID",
        "biosample": "BIOSAMPLE_ID"
    }
    phenotypicfeature["type"]["id"] = type_id
    phenotypicfeature["phenopacket"] = phenopacket_id
    phenotypicfeature["biosample"] = biosample_id
    return phenotypicfeature


def get_phenopacket(phenopacket_id, individual_id, meta_data_id, table_id, biosample_id, gene_id, variant_id, disease_id):
    '''
    returns a sample phenopacket json
    the phenopacket json contains an id as the phenopacket_id passed in
    The phenopacket is related to the individual with the individual id passed in, 
        the metadata with the metadata id passed in, the table with the table id passed in,
        the biosample with the biosample id passed in, the variant with the variant id passed in and the disease with the disease id passed in
    '''
    phenopacket = {
        "id": "PHENOPACKET_ID",
        "subject": "INDIVIDUAL_ID",
        "meta_data": 0,
        "table": "TABLE_ID",
        "biosamples": ["BIOSAMPLE_ID"],
        "genes": ["GENE_ID"],
        "variants": ["VARIANT_ID"],
        "diseases": ["DISEASE_ID"]
    }
    phenopacket["id"] = phenopacket_id
    phenopacket["subject"] = individual_id
    phenopacket["meta_data"] = meta_data_id
    phenopacket["table"] = table_id
    phenopacket["biosamples"][0] = biosample_id
    phenopacket["genes"][0] = gene_id
    phenopacket["variants"][0] = variant_id
    phenopacket["diseases"][0] = disease_id
    return phenopacket


def get_interpretation(interpretation_id, phenopacket_id, meta_data_id, diagnosis_id):
    '''
    returns a sample interpretation id
    the interpretation id contains an id as the interpretation id passed in
    The interpretation will be related to the phenopacket with the phenopacket id passed in, 
    the metadata with the metadata id passed in, and the diagnosis with the diagnosis id passed in
    '''
    interpretation = {
        "id": "INTERRPRETATION_ID",
        "phenopacket": "PHENOPACKET_ID",
        "meta_data": 0,
        "diagnosis": ["DIAGNOSIS_ID"]
    }
    interpretation["id"] = interpretation_id
    interpretation["phenopacket"] = phenopacket_id
    interpretation["meta_data"] = meta_data_id
    interpretation["diagnosis"][0] = diagnosis_id
    return interpretation


def create_sample_data(dataset_name, meta_data_id, individual_id, table_id):
    '''
    creates sample data in dataset with name as dataset_name
    '''

    biosample_id = dataset_name
    biosample = get_biosample(biosample_id, biosample_id)
    post_data(f"{KATSU_URL}/api/biosamples", biosample)

    disease = get_disease(dataset_name)
    disease_id = post_data(f"{KATSU_URL}/api/diseases", disease)["id"]

    gene = get_gene(dataset_name)
    gene_id = dataset_name
    post_data(f"{KATSU_URL}/api/genes", gene)

    variant = get_variant(dataset_name)
    variant_id = post_data(f"{KATSU_URL}/api/variants", variant)["id"]

    genomic_interpretation = get_genomic_interpretation(
        dataset_name, gene_id, variant_id)
    genomic_interpretation_id = post_data(
        f"{KATSU_URL}/api/genomicinterpretations", genomic_interpretation)["id"]

    diagnosis = get_diagnosis(dataset_name, disease_id,
                              genomic_interpretation_id)
    diagnosis_id = post_data(f"{KATSU_URL}/api/diagnoses", diagnosis)["id"]

    phenopacket_id = dataset_name
    phenopacket = get_phenopacket(dataset_name, individual_id, meta_data_id,
                                  table_id, biosample_id, gene_id, variant_id, disease_id)
    post_data(f"{KATSU_URL}/api/phenopackets", phenopacket)

    phenotypicfeature = get_phenotypicfeature(
        dataset_name, phenopacket_id, biosample_id)
    post_data(f"{KATSU_URL}/api/phenotypicfeatures", phenotypicfeature)

    interpretation_id = dataset_name
    interpretation = get_interpretation(
        interpretation_id, phenopacket_id, meta_data_id, diagnosis_id)
    post_data(f"{KATSU_URL}/api/interpretations", interpretation)


def create_project_table_meta_data(project_title):
    '''
    creates a project with the project_title passed in
    creates a meta data as it is required for creating some objects
    creates an individual as it is required for creating some objects
    creates datasets, tables and table ownerships 
    creates sample data in datasets
    '''
    project_id = get_project_id(project_title)
    meta_data_id = get_meta_data_id()
    post_data(f"{KATSU_URL}/api/individuals", {"id": "test_individual"})
    for t in ["open1", "open2", "registered3", "controlled4", "controlled5", "controlled6"]:
        dataset_id = get_dataset_id(t, project_id)
        create_table_ownership(t, dataset_id)
        create_table(t)
        create_sample_data(t, meta_data_id,
                           "test_individual", t)


title = "test"
create_project_table_meta_data(title)
