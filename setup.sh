./generate-certs.sh
touch permissions_engine/data.json
docker-compose up -d
sleep 300
./oidc/config-oidc-service
python3 permissions_engine/fetch_keys.py
docker-compose restart opa