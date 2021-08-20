function create_dataset() {
  dataset_title=${1}
  dataset_id=$(cat templates/dataset_template.json|sed s/DATASET_TITLE/${dataset_title}/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
    -H 'Content-Type: application/json' \
    --data-binary @- |jq -r .identifier)
  echo ${dataset_id}
}


function create_table() {
    table_id=${1}
    dataset_id=${2}
    cat templates/table_ownership_template.json|sed s/TABLE_ID/${table_id}/|sed s/DATASET_ID/${dataset_id}/|curl -X POST 'localhost:8001/api/table_ownership' \
    -H 'Content-Type: application/json' \
    --data-binary @-;echo

    echo "Created table ownership with table id ${table_id} for dataset ${dataset_id}";echo

    cat templates/table_template.json|sed s/TABLE_ID/${table_id}/|sed s/TABLE_NAME/table${table_id}/|curl -X POST 'localhost:8001/api/tables' \
    -H 'Content-Type: application/json' \
    --data-binary @-;echo

    echo "Created table id ${table_id} with name table${table_id}";echo
}

function create_pheno() {
    table_id=${1}
    cat templates/phenopacket_template.json|sed s/0/${METADATA_ID}/|sed s/PHENOPACKET_ID/pheno_${table_id}/|sed s/INDIVIDUAL_ID/${INDIVIDUAL_ID}/|sed s/TABLE_ID/${table_id}/|curl -X POST 'localhost:8001/api/phenopackets' \
    -H 'Content-Type: application/json' \
    --data-binary @-;echo
    echo "Created phenopacket with id pheno_${table_id}";echo
}


cd tests

export PROJECT_ID=$(curl -X POST 'localhost:8001/api/projects' -H "Content-Type: application/json" -d '{"title": "tests", "description": "Project for tests"}'|jq -r .identifier)
echo "Created project ${PROJECT_ID}";echo

export METADATA_ID=$(curl -X POST 'localhost:8001/api/metadata' -H 'Content-Type: application/json'  -d '{"created_by": "test"}' | jq .id)
echo "Created metadata with id ${METADATA_ID}";echo

export INDIVIDUAL_ID="test_individual"
curl -X POST 'localhost:8001/api/individuals' -H 'Content-Type: application/json'  -d '{"id": "test_individual"}';echo
echo "Created individual with id test_individual";echo

counter=110
for dataset_title in "open1" "open2" "registered3" "controlled4" "controlled5" "controlled6"
do
    dataset_id=$(create_dataset $dataset_title)
    echo "Created dataset ${dataset_title} ${dataset_id}";echo

    create_table $counter $dataset_id
    
    create_pheno $counter

    
    counter=$((counter+1))
done

cd ..