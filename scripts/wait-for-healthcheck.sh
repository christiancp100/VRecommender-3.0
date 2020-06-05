#!/bin/bash
# wait-for-healthcheck.sh

set -e
COUNTER=0

until [ $COUNTER -eq 10 ] || [ $(docker-compose ps | grep elastic | grep -c "Up (healthy)") -ne 0 ]; do
  echo "Elasticsearch is unavailable - sleeping"
  COUNTER=`echo $COUNTER+1 | bc`
  sleep 4
done

if [ $(docker-compose ps | grep elastic | grep -c "Up (healthy)") -ne 0 ]; then
   echo "Elasticsearch is up"
else
   echo "Elasticsearch is NOT running. Exiting bad..."
   exit 1
fi