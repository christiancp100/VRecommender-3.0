from django.test import TestCase
from djangoapi import search
from elasticsearch import Elasticsearch
import requests

class ElasticsearchTestCase(TestCase):
    def setUp(self):
        self.client = Elasticsearch("http://elasticsearch:9200")
        self.all_indices = self.client.indices.get_alias("*")

    def test_connection(self):
        status = self.client.ping()
        self.assertTrue(status)

    def test_index_existance(self):
        exist = "objects" in self.all_indices
        self.assertTrue(exist)

class QueriesTestCase(TestCase):
    def setUp(self):
        self.fieldsList = requests.get('http://llocalhost:8000/columns')
    # TODO
    # def test_describe_query(self):
    #     for field in self.fieldsList:
    #         if field['type'] == numerical:
    #             response = requests.get('http://localhost:8000/describe/?column=' + field['value'])
    #             if responsep['count']



class EndPointsTestCase(TestCase):
    def setUp(self):
        pass
