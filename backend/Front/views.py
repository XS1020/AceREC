from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
import json
# Create your views here.
import pysolr
from apis.utils import Get_Paper_Ref
from Const_Var import Paper_Subset
from Const_Var import Author_Subset
from Const_Data_Base import History_Graph
from random import shuffle
from apis.utils import Local_to_Remote
from .utils import Recomend_Author_by_Author


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


def Get_Search_Res(keyword, stype='All', start=0, solrlink=None):
    if solrlink is None:
        solrlink = pysolr.Solr('http://localhost:8983/solr/EE447', timeout=300)
    keyword = '+'.join(keyword.split())

    if stype not in ['All', 'Title', 'Author', 'Conference', 'Journal']:
        raise ValueError('Not a legal search type')

    if stype == 'All':
        result = solrlink.search('search:%s' % keyword, rows=20, start=start)
    if stype == 'Title':
        result = solrlink.search('title:%s' % keyword, rows=20, start=start)
    if stype == 'Author':
        result = solrlink.search('author_name:%s' %
                                 keyword, rows=20, start=start)
    if stype == 'Conference':
        result = solrlink.search('conference:%s' %
                                 keyword, rows=20, start=start)
    if stype == 'Journal':
        result = solrlink.search('journal:%s' % keyword, rows=20, start=start)

    return result


def Search(request):
    Data = request.GET
    if not Data:
        return HttpResponseBadRequest('No Data')
    if 'keyword' not in Data:
        return HttpResponseBadRequest('No Data')
    Solr = pysolr.Solr('http://localhost:8983/solr/EE447', timeout=300)

    search_type = Data.get('mode', 'All')
    try:
        Page_num = int(Data.get('page', 1))
        Start = (Page_num - 1) * 20
    except Exception as e:
        return HttpResponseNotAllowed("Not Int Page_num")

    if Start < 0:
        return HttpResponseNotAllowed("Start Place should be non-negative")

    keyword = Data['keyword']

    try:
        result = Get_Search_Res(keyword, search_type, Start, Solr)
    except Exception as e:
        return HttpResponseNotAllowed(str(e))

    # result = Get_Search_Res(keyword, search_type, Start, Solr)

    Paperid_list = [res['paperid'] for res in result]
    return JsonResponse({
        'paper_id_list': Paperid_list,
        'number': result.hits
    })


def Recomend_and_cite_Paper_Page(request):
    Data = request.GET
    if not Data or 'paperid' not in Data:
        return HttpResponseBadRequest("No \"paperid\" Found")

    try:
        paperid = int(Data['paperid'])
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


def Recomend_Author(request):
    Data = request.GET
    if not Data:
        return HttpResponseBadRequest("No Data Found")

    local_id = Data.get('local_id', None)
    if local_id is None:
        As = list(Author_Subset)
        shuffle(As)
        return JsonResponse({"Rec_Authors": As[:5]})

    try:
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int local id")

    remote_id = Local_to_Remote(local_id)
    print(len(History_Graph.User_History.get(remote_id, [])))
    if len(History_Graph.User_History.get(remote_id, [])) < 10:
        As = list(Author_Subset)
        shuffle(As)
        return JsonResponse({"Rec_Authors": As[:5]})

    else:
        Rec_Authors = Recomend_Author_by_Author(remote_id, 20, 20)
        return JsonResponse({'Rec_Authors': [x[0] for x in Rec_Authors]})
