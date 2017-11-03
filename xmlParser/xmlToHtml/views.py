# -*- coding: utf-8 -*-
import json
import urllib
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from elasticsearch import Elasticsearch


def search_view(request):
    return render(request, 'xmlToHtml/index.html', {})


def search_filter(request):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    query = urllib.unquote(request.get_full_path())
    query_array = query.split('?q=')[1].split('&')
    q_dict = dict()
    for item in query_array:
        if item.find('=') != -1:
            key = item.split('=')[0].encode()
            val = urllib.unquote(item.split('=')[1]).encode()
            if key in q_dict:
                lst = q_dict[key]
                lst.append(val)
                q_dict[key] = lst
            else:
                q_dict[key] = [val]
    qry = q_dict['query'][0]
    q2 = {
        "size": 2000,
        "query": {
            "bool": {
                "must": {
                    "bool": {
                        "should": [
                            {
                                "multi_match": {
                                    "query": qry,
                                    "fields": ["_all"]
                                }
                            },
                            {
                                "multi_match": {
                                    "query": qry,
                                    "fields": [
                                        "member1_name",
                                        "member2_name",
                                        "member3_name",
                                        "title_symbol"
                                    ]
                                }
                            }
                        ],
                        "must": []
                    }
                }
            }
        }
    }
    if 'research-type' in q_dict:
        bool_query = {"bool": {"should": []}}
        for item in q_dict["research-type"]:
            dic = dict()
            dic['match'] = {"research_type": item}
            bool_query['bool']['should'].append(dic)
        q2["query"]["bool"]["must"]["bool"]["must"].append(bool_query)

    if 'performance' in q_dict:
        bool_query = {"bool": {"should": []}}
        for item in q_dict['performance']:
            dic = dict()
            dic['match'] = {"performance": item}
            bool_query['bool']['should'].append(dic)
        q2["query"]["bool"]["must"]["bool"]["must"].append(bool_query)

    if 'country' in q_dict:
        bool_query = {"bool": {"should": []}}
        for item in q_dict['country']:
            dic = dict()
            dic['match'] = {"country": item}
            bool_query['bool']['should'].append(dic)
        q2["query"]["bool"]["must"]["bool"]["must"].append(bool_query)

    resp = es.search(index='bmo_capital_markets', doc_type='', body=q2)
    resp = json.dumps(resp)
    return JsonResponse(
        {
            'success': True,
            'response': resp
        }
    )


def search(request):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    query_str = request.get_full_path().split('?q=')[1]
    q1 = {
        "size": 50,
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query_str,
                            "fields": ["_all"]
                        }
                    },
                    {
                        "multi_match": {
                            "query": query_str,
                            "fields": [
                                "member1_name",
                                "member2_name",
                                "member3_name",
                                "member1_email",
                                "member2_email",
                                "member3_email",
                            ]
                        }
                    }
                ]
            },
        }
    }

    q2 = {
        "size": 50,
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": query_str,
                            "fields": ["_all"]
                        }
                    },
                    {
                        "multi_match": {
                            "query": query_str,
                            "fields": [
                                "investment_vehicleid",
                            ]
                        }
                    }
                ]
            },
        }
    }

    resp = {}

    # import ipdb; ipdb.set_trace()
    resp['research_data'] = es.search(index='bmo_capital_markets', doc_type='research_data', body=q1)
    resp['company_data'] = es.search(index='bmo_capital_markets', doc_type='company_data', body=q2)


    return JsonResponse(
        {
            'success': True,
            'response': resp
        }
    )


def show_document(request, doc_name):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    query = {
        "query": {
            "match": {
                "_all": {
                    "query": doc_name.encode('utf-8')
                }
            }
        }
    }

    resp = es.search(index='bmo_capital_markets', doc_type='', body=query)
    context = resp.get('hits').get('hits')[0]['_source']
    return render(request, 'xmlToHtml/output.html', context)

def show_company(request, company):
    es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
    query = {
        "query": {
            "match": {
                "investment_vehicleid": company.encode('utf-8')
            }
        }
    }

    resp = es.search(index='bmo_capital_markets', doc_type='', body=query)
    context = resp.get('hits').get('hits')[0]['_source']
    return render(request, 'xmlToHtml/company.html', context)
