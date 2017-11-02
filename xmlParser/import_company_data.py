import os
import datetime
import random
import json

# from django.template import Context, Template
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
# from threading import Thread
from io import StringIO, BytesIO

file_path = os.path.join(os.getcwd(), 'mf') + '.json'

with open(file_path) as data_file:
    data = json.load(data_file)

count = 0
company_data = list()

es_settings = {
    "settings": {
        "analysis": {
            "filter": {
                "edge_nGram_filter": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 20,
                    "token_chars": [
                        "letter",
                        "digit"
                    ]
                }
            },
            "analyzer": {
                "edge_nGram_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "asciifolding",
                        "edge_nGram_filter"
                    ]
                },
                "whitespace_analyzer": {
                    "type": "custom",
                    "tokenizer": "whitespace",
                    "filter": [
                        "lowercase",
                        "asciifolding"
                    ]
                }
            }
        }
    },
    "mappings": {
        "company_data": {
            "properties": {
                "investment_vehicleid": {
                    "type": "string",
                    "analyzer": "edge_nGram_analyzer",
                    "search_analyzer": "whitespace_analyzer"
                },
            }
        }
    }
}
# "name_en": {
#     "type": "string",
#     "analyzer": "edge_nGram_analyzer",
#     "search_analyzer": "whitespace_analyzer"
# },

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

try:
	# es.indices.delete(index='bmo_capital_markets')
	es.indices.create(index='bmo_capital_markets', body=es_settings)
	# XMLData.objects.all().delete()
except Exception as inst:
	print str(inst)
	# es.indices.create(index='bmo_capital_markets', body=es_settings)

for row in data['hits']['hits']:

	row['_index'] = 'bmo_capital_markets'
	row['_type'] = 'company_data'

	company_data.append(row)

	if count == 1000:
		count = 0
		bulk(es, company_data, index = 'bmo_capital_markets', raise_on_error=True)
		company_data = list()
		print "1000 %s Records Indexed"

	count += 1