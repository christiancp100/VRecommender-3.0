from django.contrib.gis.db import models
#from djangoapi.documents import ObjectDocument
from elasticsearch import Elasticsearch
from django.utils.translation import gettext_lazy as _
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)

from django_elasticsearch_dsl import (
    Document,
    fields,
    Index,
)

from django_elasticsearch_dsl_drf.compat import KeywordField, StringField

object_index = Index('objects')

object_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

client = Elasticsearch("http://elasticsearch:9200")

class Object(models.Model):
    class Meta:
        es_index_name = 'objects'
        es_type_name = 'objects'
        es_mapping = client.indices.get_mapping('objects')['objects']['mappings']
        
@object_index.doc_type
class ObjectDocument(Document):

    class Django:
        model = Object  

