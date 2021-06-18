cd tests

export PROJECT_ID=$(curl -X POST 'localhost:8001/api/projects' -H "Content-Type: application/json" -d '{"title": "tests", "description": "Project for tests"}'|jq -r .identifier)
echo "Created project ${PROJECT_ID}";echo

export OPEN_DATASET1_ID=$(cat dataset_template.json|sed s/DATASET_TITLE/open1/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
-H 'Content-Type: application/json' \
--data-binary @- |jq -r .identifier)
echo "Created open dataset 1 ${OPEN_DATASET1_ID}";echo

export OPEN_DATASET2_ID=$(cat dataset_template.json|sed s/DATASET_TITLE/open2/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
-H 'Content-Type: application/json' \
--data-binary @- |jq -r .identifier)
echo "Created open dataset 2 ${OPEN_DATASET2_ID}";echo

export REGISTERED_DATASET3_ID=$(cat dataset_template.json|sed s/DATASET_TITLE/registered3/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
-H 'Content-Type: application/json' \
--data-binary @- |jq -r .identifier)
echo "Created registered dataset 3 ${REGISTERED_DATASET3_ID}";echo

export CONTROLLED_DATASET4_ID=$(cat dataset_template.json|sed s/DATASET_TITLE/controlled4/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
-H 'Content-Type: application/json' \
--data-binary @- |jq -r .identifier)
echo "Created controlled dataset 4 ${CONTROLLED_DATASET4_ID}";echo

export CONTROLLED_DATASET5_ID=$(cat dataset_template.json|sed s/DATASET_TITLE/controlled5/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
-H 'Content-Type: application/json' \
--data-binary @- |jq -r .identifier)
echo "Created controlled dataset 5 ${CONTROLLED_DATASET5_ID}";echo

export CONTROLLED_DATASET6_ID=$(cat dataset_template.json|sed s/DATASET_TITLE/controlled6/|sed s/PROJECT_ID/${PROJECT_ID}/|curl -X POST 'localhost:8001/api/datasets' \
-H 'Content-Type: application/json' \
--data-binary @- |jq -r .identifier)
echo "Created controlled dataset 6 ${CONTROLLED_DATASET6_ID}";echo

export METADATA_ID=$(curl -X POST 'localhost:8001/api/metadata' -H 'Content-Type: application/json'  -d '{"created_by": "test"}' | jq .id)
echo "Created metadata with id ${METADATA_ID}";echo

export INDIVIDUAL_ID="test_individual"
curl -X POST 'localhost:8001/api/individuals' -H 'Content-Type: application/json'  -d '{"id": "test_individual"}';echo
echo "Created individual with id test_individual";echo

counter=1
for i in $OPEN_DATASET1_ID $OPEN_DATASET2_ID $REGISTERED_DATASET3_ID $CONTROLLED_DATASET4_ID $CONTROLLED_DATASET5_ID $CONTROLLED_DATASET6_ID
do
    cat table_ownership_template.json|sed s/TABLE_ID/${counter}/|sed s/DATASET_ID/${i}/|curl -X POST 'localhost:8001/api/table_ownership' \
    -H 'Content-Type: application/json' \
    --data-binary @-;echo
    echo "Created table ownership with table id ${counter} for dataset ${i}";echo

    cat table_template.json|sed s/TABLE_ID/${counter}/|sed s/TABLE_NAME/table${counter}/|curl -X POST 'localhost:8001/api/tables' \
    -H 'Content-Type: application/json' \
    --data-binary @-;echo
    echo "Created table id ${counter} with name table${counter}";echo

    cat phenopacket_template.json|sed s/0/${METADATA_ID}/|sed s/PHENOPACKET_ID/pheno_${counter}/|sed s/INDIVIDUAL_ID/${INDIVIDUAL_ID}/|sed s/TABLE_ID/${counter}/|curl -X POST 'localhost:8001/api/phenopackets' \
    -H 'Content-Type: application/json' \
    --data-binary @-;echo
    echo "Created phenopacket with id pheno_${counter}";echo
    counter=$((counter+1))
done

cd ..