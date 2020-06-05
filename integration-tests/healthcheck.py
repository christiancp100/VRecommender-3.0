from requests import get
import logging
import sys

critical = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

elastic = None
try:
   elastic = get("http://elasticsearch:9200/_cluster/health")
   assert elastic.status_code == 200
   assert elastic.json()["status"] != "red"
   logger.info("Elasticsearch on port 9200: .......RUNNING")
except:
   logger.critical("Elasticsearch is not up and running.")
   if elastic:
      logger.critical(f"\nResponse: {elastic.json()}", exc_info=True)
   critical = True

django = None
try:
   django = get("http://django-backend:8000/healthcheck")
   assert django.status_code == 200
   logging.info("Django on port 8000: ..............RUNNING")
except:
   logger.critical("Django is not up and running.")
   if django:
      logger.critical(f"Status: {django.status_code}\nResponse: {django.text[:500]}", exc_info=True)
   critical = True

vuejs = None
try:
   vuejs = get("http://vuejs-frontend:8080/healthcheck")
   assert vuejs.status_code == 200
   logging.info("Vue on port 8080: .................RUNNING")
except:
   logger.critical("VueJS is not up and running.")
   if vuejs:
      logger.critical(f"\nStatus: {vuejs.status_code}\nResponse: {vuejs.text[:500]}", exc_info=True)
   critical = True


if critical:
   logging.error("Critical exceptions were thrown, exiting bad.")
   sys.exit(-1)