from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
import time
from User.models import User_Token
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
import os
from Const_Var import Paper_Pdf_Mapping
from Const_Var import Author_Subset
from backend.settings import STATICFILES_DIRS
import MySQLdb
import MySQLdb.cursors
import datetime
from .utils import Get_Conn_Paper, Get_Conn_Analysis, close_conn
from .models import Record
from .utils import Get_Paper_Conf, Get_Paper_Jour, Get_Citation_Trend
from .utils import Get_Author_List, Get_Paper_Citation
from .utils import Get_Paper_Abstract, Get_Org_Url, Get_Paper_Doi
from .utils import Get_Paper_Keyword, Get_Paper_Doi, Get_Org_Url
from .utils import Remote_to_Local, Local_to_Remote
from .utils import Get_Person_Cite, Get_Related_Authors
from .utils import Get_Person_Cite_Count, Get_Person_Record
from User.views import LOGIN_TIME_OUT
# Create your views here.


def Cover_Url(request, paperid):
    imgdir = os.path.join(STATICFILES_DIRS[0], 'pdf_img')
    if str(paperid) in Paper_Pdf_Mapping:
        imgname = Paper_Pdf_Mapping[str(paperid)]
        imgname = imgname[:-3] + 'png'
        if os.path.exists(os.path.join(imgdir, imgname)):
            return '{}://{}/static/pdf_img/{}'.format(
                request.scheme, request.get_host(), imgname
            )
    return ''


def Main_Page_Card_Info(request):
    Data = request.GET

    # Error Part
    if not Data:
        return HttpResponseBadRequest('No \"paperid\" Found')
    paperid = Data.get('paperid', None)
    if paperid is None:
        return HttpResponseBadRequest('No \"paperid\" Found')
    try:
        paperid = int(paperid)
    except ValueError as e:
        return HttpResponseNotAllowed('Not Int Paperid')

    (conn, cursor), dRes = Get_Conn_Paper(), {}
    cursor.execute(
        'SELECT title, year, journal_id, conference_series_id \
         from am_paper where paper_id={}'.format(paperid)
    )
    confind, jourid, IsLine = 0, 0, False
    for lin in cursor:
        dRes['year'], dRes['title'] = lin[1], lin[0]
        jourid, confind, IsLine = lin[2], lin[3], True

    if not IsLine:
        close_conn(conn, cursor)
        return HttpResponseBadRequest('No Such Paper')

    dRes['conference'], dRes['Abbr'] = '', ''

    if confind != 0:
        Conf = Get_Paper_Conf(confind, cursor)
        if Conf != None:
            dRes.update(Conf)
    if jourid != 0:
        Jour = Get_Paper_Jour(jourid, cursor)
        if Jour != None:
            dRes.update(Jour)

    dRes['author_name_list'] = []
    dRes['author_id_list'] = []
    dRes['abstract'] = ''
    dRes.update(Get_Author_List(paperid, cursor))
    Abs = Get_Paper_Abstract(paperid, cursor)
    if Abs != None:
        dRes.update(Abs)

    dRes['imgurl'] = Cover_Url(request, paperid)

    dRes['citation_count'] = 0
    dRes.update(Get_Paper_Citation(paperid))
    """
    print(request.path_info)
    print(request.scheme)
    print(request.get_host())
    """
    close_conn(conn, cursor)

    return JsonResponse(dRes)


def Generate_cite_name(title, year, author_name_list):
    title_part = title.split()[0]
    year_part = str(year)
    author_part = []
    if len(author_name_list) > 0:
        for x in author_name_list[0]:
            if x.isalpha():
                author_part.append(x)
            else:
                break

    return ''.join(author_part) + year_part + title_part


def Generate_Paper_bibtex(request):
    Data = request.GET
    if not Data or 'paperid' not in Data:
        return HttpResponseBadRequest('No \"paperid\" Found')
    try:
        paperid = int(Data['paperid'])
    except ValueError as e:
        return HttpResponseNotAllowed('Not a Int Paperid')

    conn, cursor = Get_Conn_Paper()
    cursor.execute(
        'SELECT paper_id, title, year, journal_id, \
        conference_series_id, volume, first_page, last_page\
        from am_paper where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchone()
    if not Ans:
        close_conn(conn, cursor)
        return HttpResponseBadRequest('No Such Paper')

    paper_id, title, year = Ans[0], Ans[1], Ans[2]
    jourid, confid = Ans[3], Ans[4]
    vol, fpage, lpage = Ans[5], Ans[6], Ans[7]
    if confid != 0:
        Conf = Get_Paper_Conf(confid, cursor)
    if jourid != 0:
        Jour = Get_Paper_Jour(jourid, cursor)

    Auinfo = Get_Author_List(paperid, cursor)

    Answer = """@article{ %s,
    title = {%s},
    author = {%s},
    %s %s %s %s %s}""" % (
        Generate_cite_name(title, year, Auinfo['author_name_list']),
        title, ' and '.join(Auinfo['author_name_list']).replace('.', ' '),
        'year = {{{}}},\n'.format(year) if year != 0 else '',
        'booktitle = {{ {} }},\n'.format(
            Conf['conference']
        ) if confid != 0 else '',
        'journal={{ {} }},\n'.format(
            Jour['conference']
        ) if jourid != 0 else '',
        'volume={{{}}},\n'.format(vol) if vol != 0 else '',
        'pages={{{}--{}}},\n'.format(fpage, lpage) if lpage != 0 else ''
    )

    close_conn(conn, cursor)
    return JsonResponse({'bib': Answer})


@csrf_exempt
def Add_View_recoed(request):
    Data = request.POST

    if not Data or 'local_id' not in Data or 'paper_id' not in Data:
        return JsonResponse({'stat': 0, 'Reason': "No Sufficient Data"})

    try:
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Ids")

    if local_id < 0:
        return JsonResponse({"stat": 0, 'Reason': "No Such Person"})

    remote_id = Local_to_Remote(local_id)
    if remote_id < -1:
        return JsonResponse({"stat": 0, 'Reason': "No Such Person"})

    Token = request.META.get('HTTP_TOKEN', "")

    Obj = User_Token.objects.filter(local_id=local_id)
    if len(Obj) == 0 or Token != Obj[0].token:
        return HttpResponse('Unauthorlized', status=401)

    if time.time() - Obj[0].update_time > LOGIN_TIME_OUT:
        return HttpResponse('Unauthorlized', status=401)

    paper_id_list = []
    for paperid in Data['paper_id'].split(','):
        try:
            paperid = int(paperid)
        except ValueError as e:
            return HttpResponseNotAllowed("Not Int Paperid")
        paper_id_list.append(paperid)

    for paper_id in paper_id_list:
        Record.objects.create(
            paper_id=paper_id, local_id=local_id,
            remote_id=remote_id, rtype=1
        )

    return JsonResponse({"stat": 1, "Reason": ""})


@csrf_exempt
def Add_Click_record(request):
    Data = request.POST

    if not Data or 'local_id' not in Data or 'paper_id' not in Data:
        return JsonResponse({'stat': 0, 'Reason': "No Sufficient Data"})

    try:
        paper_id = int(Data['paper_id'])
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Ids")

    if local_id < 0:
        return JsonResponse({"stat": 0, 'Reason': "No Such Person"})

    remote_id = Local_to_Remote(local_id)
    if remote_id < -1:
        return JsonResponse({"stat": 0, 'Reason': "No Such Person"})

    Token = request.META.get('HTTP_TOKEN', "")
    Obj = User_Token.objects.filter(local_id=local_id)
    if len(Obj) == 0 or Token != Obj[0].token:
        return HttpResponse('Unauthorlized', status=401)
    if time.time() - Obj[0].update_time > LOGIN_TIME_OUT:
        return HttpResponse('Unauthorlized', status=401)

    Record.objects.create(
        paper_id=paper_id, local_id=local_id,
        remote_id=remote_id, rtype=2
    )

    return JsonResponse({"stat": 1, "Reason": ""})


def Paper_Citation_Trend(request):
    Data = request.GET

    if not Data or 'paperid' not in Data:
        return HttpResponseBadRequest("No PaperId Found")

    try:
        paperid = int(Data['paperid'])
    except ValueError as e:
        return HttpResponseNotAllowed('Not a Int Paperid')

    Cite_trend = Get_Citation_Trend(paperid)
    Cite_trend.sort(key=lambda x: x['year'])

    return JsonResponse({'cite_trend': Cite_trend})


def Paper_Page_Info(request):
    Data = request.GET

    if not Data or 'paperid' not in Data:
        return HttpResponseBadRequest("No PaperId Found")

    try:
        paperid = int(Data['paperid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not a Int Paperid")

    conn, cursor = Get_Conn_Paper()

    cursor.execute(
        'SELECT title, doi, year from am_paper\
        where paper_id = {}'.format(paperid)
    )

    BasInfo = cursor.fetchone()

    if not BasInfo:
        close_conn(conn, cursor)
        return HttpResponseBadRequest("No Such Paper")

    title, doi, year = BasInfo
    DAns = {'title': title, 'doi': doi, 'year': year}

    DAns['imgurl'] = Cover_Url(request, paperid)

    DAns['citation_count'] = 0
    DAns.update(Get_Paper_Citation(paperid))
    DAns['abstract'] = ''
    Abs = Get_Paper_Abstract(paperid, cursor)
    if Abs:
        DAns.update(Abs)
    Author_Info = Get_Author_List(paperid, cursor)
    RtoL = Remote_to_Local(Author_Info['author_id_list'])

    DAns['Authors'] = []
    for i, name in enumerate(Author_Info['author_name_list']):
        remote_id = Author_Info['author_id_list'][i]
        DAns['Authors'].append({
            'name': name, 'remote_id': remote_id,
            'local_id': RtoL[remote_id],
            'clickable': 1 if remote_id in Author_Subset else 0
        })

    DAns.update(Get_Org_Url(paperid, cursor))

    close_conn(conn, cursor)
    return JsonResponse(DAns)


def Paper_Keyword(request):
    Data = request.GET

    if not Data or 'paperid' not in Data:
        return HttpResponseBadRequest("Not PaperId Found")

    try:
        paperid = int(Data['paperid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not a Int Paperid")

    keywords = Get_Paper_Keyword(paperid, 'text', 'size')

    return JsonResponse({'keyword': keywords})


def Person_Cite_Trend(request):
    Data = request.GET

    if not Data or 'local_id' not in Data:
        return HttpResponseBadRequest("No local_id Found")

    try:
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Local_id")

    remote_id = Local_to_Remote(local_id)
    if remote_id < 0:
        return HttpResponseBadRequest("No Such Person")

    Cite_trend = Get_Person_Cite(remote_id)
    Cite_trend.sort(key=lambda x: x['year'])
    return JsonResponse({'trend': Cite_trend})


def Cite_Card_Info(request):
    Data = request.GET
    if not Data or 'paperid' not in Data:
        return HttpResponseBadRequest("No PaperId Found")

    try:
        paperid = int(Data['paperid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int paperid")

    conn, cursor = Get_Conn_Paper()

    cursor.execute(
        'SELECT title, year from am_paper\
        where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchone()
    if not Ans:
        close_conn(conn, cursor)
        return HttpResponseBadRequest("No Such Paper")

    title, year = Ans

    Dans = {'title': title, 'year': year}
    Author_Info = Get_Author_List(paperid, cursor)
    Dans.update(Author_Info)

    Tags = Get_Paper_Keyword(paperid, cursor=cursor)
    Tags.sort(key=lambda x: -x['level'])
    Dans['tags'] = [x['keyword'] for x in Tags if x['level'] > 1]

    close_conn(conn, cursor)

    Dans['imgurl'] = Cover_Url(request, paperid)

    return JsonResponse(Dans)


def Related_Author(request):
    Data = request.GET

    if not Data or 'local_id' not in Data:
        return HttpResponseBadRequest("No Author Id")

    try:
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Local_id")
    remote_id = Local_to_Remote(local_id)
    if remote_id < 0:
        return JsonResponse({'Related': []})
    Rel_Aut_cnt = Get_Related_Authors(remote_id)
    Cans = list(Rel_Aut_cnt.keys())
    Cans.sort(key=lambda x: -Rel_Aut_cnt[x])

    Ans = []
    Loc_id = Remote_to_Local(Cans)
    for remid in Cans[:4]:
        Ans.append({
            'remote_id': remid, 'local_id': Loc_id[remid],
            'clickable': 1 if remid in Author_Subset else 0
        })

    return JsonResponse({"Related": Ans})


def Author_Cite_Count(request):
    Data = request.GET
    if not Data or 'local_id' not in Data:
        return HttpResponseBadRequest('No Local id')

    try:
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed('Not Int Id')

    remote_id = Local_to_Remote(local_id)
    Ans = Get_Person_Cite_Count(remote_id)
    if not Ans:
        return JsonResponse({
            'citation_count': 0,
            'paper_count': 0,
            'h_index': 0
        })
    else:
        return JsonResponse({
            "citation_count": Ans[0],
            'paper_count': Ans[1],
            'h_index': Ans[2]
        })


def ctoken(request):
    token = get_token(request=request)
    return JsonResponse({'token': token})


def Get_User_Record(request):
    Data = request.GET
    if not Data or 'local_id' not in Data:
        return HttpResponseBadRequest("No localid found")
    try:
        local_id = int(Data['local_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Id")

    Records = Get_Person_Record(local_id)
    Pids = set()
    for lin in Records:
        lin['time'] = lin['time'].strftime("%Y-%m-%d %H:%M:%S")
        Pids.add(lin['paperid'])
    if len(Pids) == 0:
        return JsonResponse({'record': []})

    conn, cursor = Get_Conn_Paper()
    Pid2title = {}
    cursor.execute(
        'SELECT title, paper_id from am_paper\
        where paper_id in ({})'.format(','.join(str(x) for x in Pids))
    )
    for lin in cursor:
        Pid2title[lin[1]] = lin[0]
    close_conn(conn, cursor)
    for lin in Records:
        lin['title'] = Pid2title[lin['paperid']]

    return JsonResponse({'record': Records[:20]})
