import os
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
# from threading import Thread


print ("Process started")

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
                "ticker": {
                    "type": "string",
                    "analyzer": "edge_nGram_analyzer",
                    "search_analyzer": "whitespace_analyzer"
                },
            }
        }
    }
}

es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

try:
    es.indices.delete(index='bmo_capital_markets')
    es.indices.create(index='bmo_capital_markets', body=es_settings)
    # XMLData.objects.all().delete()
except Exception as err:
    print (err)
    # es.indices.create(index='bmo_capital_markets', body=es_settings)

total = len(data)

for company in data:
    row = {}
    row['_index'] = 'bmo_capital_markets'
    row['_type'] = 'company_data'
    row['_source'] = company
    company_data.append(row)

    if count == 500:
        count = 0
        bulk(es, company_data, index='bmo_capital_markets', raise_on_error=True)
        company_data = list()
        total = total - 500

    count += 1

    if count == total:
        bulk(es, company_data, index='bmo_capital_markets', raise_on_error=True)
print ("Process ended")
