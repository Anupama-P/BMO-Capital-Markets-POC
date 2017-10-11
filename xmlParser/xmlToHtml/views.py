# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from elasticsearch import Elasticsearch


def search_view(request):
    return render(request, 'xmlToHtml/index.html', {})


def search(request):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    query_str = request.get_full_path().split('?q=')[1]
    query = {
        "size": 50,
        "query": {
            "match": {
                "_all": {
                    "query": query_str
                }
            }
        }
    }
    q2 = {
        "size": 2000,
        "query": {
            "bool": {
                "should": [{
                    "multi_match": {
                        "query": query_str,
                        "fields": ["_all"]
                    }
                }, {
                    "multi_match": {
                        "query": query_str,
                        "fields": [
                            "member1_name",
                            "member2_name",
                            "member3_name",
                            "member1_email",
                            "member2_email",
                            "member3_email",
                            "country",
                            "research_type"
                        ]
                    }
                }]
            },
        }
    }
    resp = es.search(index='xml_data', doc_type='xml_body', body=q2)
    resp = json.dumps(resp)
    return JsonResponse(
        {
            'success': True,
            'response': resp
        }
    )


def show_document(request, doc_name):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    query = {
        "query": {
            "match": {
                "_all": {
                    "query": doc_name.encode('utf-8')
                }
            }
        }
    }

    resp = es.search(index='xml_data', doc_type='xml_body', body=query)
    context = resp.get('hits').get('hits')[0]['_source']
    return render(request, 'xmlToHtml/output.html', context)
