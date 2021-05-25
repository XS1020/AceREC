from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
import json
# Create your views here.
import pysolr


def MainPage(request):
    Recom = [
        94747717, 172379530, 216802878, 223658030, 228111136,
        277256906, 448852786, 473532210, 111870135, 379921807
    ]
    dresponse = {
        'Rec': Recom
    }
    return JsonResponse(dresponse)


def Get_Search_Res(keyword, stype='full', solrlink=None):
    if solrlink is None:
        Solr = pysolr.Solr('http://localhost:8983/solr/EE447', timeout=300)
    keyword = '+'.join(keyword.split())
    if stype not in ['full', 'title', 'author_name', 'cf_jor']:
        raise ValueError('Not a legal search type')
    if stype == 'full':
        result = Solr.search('search:%s' % keyword)
    if stype == 'title':
        result = Solr.search('title:%s' % keyword)
    if stype == 'author_name':
        result = Solr.search('author_name:%s' % keyword)
    if stype == 'cf_jor':
        result1 = Solr.search('conference:%s' % keyword)
        result2 = Solr.search('journal:%s' % keyword)
        result = result1 + result2
    return result


def Search(request):
    Data = request.GET
    if not Data:
        return HttpResponseBadRequest('No Data')
    if 'keyword' not in Data:
        return HttpResponseBadRequest('No Data')
    Solr = pysolr.Solr('http://localhost:8983/solr/EE447', timeout=300)
    search_type = Data.get('type', 'full')
    keyword = Data['keyword']
    try:
        result = Get_Search_Res(keyword, search_type, Solr)
    except Exception as e:
        return HttpResponseNotAllowed(str(e))

    Paperid_list = [res['paperid'] for res in result]
    return JsonResponse({'paper_id_list': Paperid_list})
