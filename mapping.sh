curl -X DELETE "localhost:9200/index"
curl -X PUT "localhost:9200/index" -H 'Content-Type: application/json' --data-binary @mapping.json
