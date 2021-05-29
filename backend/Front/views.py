from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
import json
# Create your views here.
import pysolr
from apis.utils import Get_Paper_Ref
from Const_Var import Paper_Subset


def MainPage(request):
    Recom = [
        94747717, 172379530, 216802878, 223658030, 228111136,
        277256906, 448852786, 473532210, 111870135, 379921807,
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
        result = solrlink.search('search:%s' % keyword)
    if stype == 'title':
        result = solrlink.search('title:%s' % keyword)
    if stype == 'author_name':
        result = solrlink.search('author_name:%s' % keyword)
    if stype == 'cf_jor':
        result1 = solrlink.search('conference:%s' % keyword)
        result2 = solrlink.search('journal:%s' % keyword)
        result = result1 + result2
    return result


def Search(request):
    Data = request.GET
    if not Data:
        return HttpResponseBadRequest('No Data')
    if 'keyword' not in Data:
        return HttpResponseBadRequest('No Data')
    Solr = pysolr.Solr('http://localhost:8983/solr/EE447', timeout=300)
    search_type = Data.get('stype', 'full')
    keyword = Data['keyword']

    try:
        result = Get_Search_Res(keyword, search_type, Solr)
    except Exception as e:
        return HttpResponseNotAllowed(str(e))

    # result = Get_Search_Res(keyword, search_type, Solr)
    Paperid_list = [res['paperid'] for res in result]
    return JsonResponse({'paper_id_list': Paperid_list})


def Recomend_and_cite_Paper_Page(request):
    Data = request.GET
    if not Data or 'paper_id' not in Data:
        return HttpResponseBadRequest("No \"paperid\" Found")

    try:
        paperid = int(Data['paper_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int paperid")

    Recom = [
        94747717, 172379530, 216802878, 223658030, 228111136
    ]

    Ans = {'Rec': Recom, 'Ref': []}
    Refs = Get_Paper_Ref(paperid)
    if Refs:
        Ans.update(Refs)

    Ans['Clickable'] = [1 if x in Paper_Subset else 0 for x in Ans['Ref']]

    return JsonResponse(Ans)
