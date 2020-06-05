#!/bin/bash
# Do it once to ingest mapping and one row of data
# Needed for the pipeline

# Create the index
curl -X PUT http://elasticsearch:9200/objects

# Put the mapping read from dataset/mapping.json
curl -X PUT http://elasticsearch:9200/objects/_mapping --data-binary @dataset/mapping.json -H "Content-type: application/json" 

# Ingest one row of data
curl -X POST http://elasticsearch:9200/objects/_bulk -H "Content-Type: application/x-ndjson" --data-binary @dataset/dataset1row.ndjson
