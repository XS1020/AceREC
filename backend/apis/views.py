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
# Create your views here.


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

    dRes['imgurl'] = ''
    imgdir = os.path.join(STATICFILES_DIRS[0], 'pdf_img')
    if str(paperid) in Paper_Pdf_Mapping:
        imgname = Paper_Pdf_Mapping[str(paperid)]
        imgname = imgname[:-3] + 'png'
        if os.path.exists(os.path.join(imgdir, imgname)):
            dRes['imgurl'] = '{}://{}/static/pdf_img/{}'.format(
                request.scheme, request.get_host(), imgname
            )
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


def Add_View_recoed(request):
    Data = request.POST

    if not Data or 'local_id' not in Data:
        return JsonResponse({'stat': 0, 'Reason': "No Sufficient Data"})
    if 'remote_id' not in Data or 'paper_id' not in Data:
        return JsonResponse({'stat': 0, 'Reason': "No Sufficient Data"})

    try:
        paper_id = int(Data['paper_id'])
        local_id, remote_id = int(Data['local_id']), int(Data['remote_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Ids")

    for paper_id in paper_id_list:
        Record.objects.create(
            paper_id=paper_id, local_id=local_id,
            remote_id=remote_id, rtype=1
        )

    return JsonResponse({"stat": 1, "Reson": ""})


def Add_Click_record(request):
    Data = request.POST

    if not Data or 'local_id' not in Data:
        return JsonResponse({'stat': 0, 'Reason': "No Sufficient Data"})
    if 'remote_id' not in Data or 'paper_id' not in Data:
        return JsonResponse({'stat': 0, 'Reason': "No Sufficient Data"})
    try:
        paper_id = int(Data['paper_id'])
        local_id, remote_id = int(Data['local_id']), int(Data['remote_id'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Ids")

    Record.objects.create(
        paper_id=paper_id, local_id=local_id,
        remote_id=remote_id, rtype=2
    )

    return JsonResponse({"stat": 1, "Reson": ""})


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

    DAns['imgurl'] = ''
    imgdir = os.path.join(STATICFILES_DIRS[0], 'pdf_img')
    if str(paperid) in Paper_Pdf_Mapping:
        imgname = Paper_Pdf_Mapping[str(paperid)]
        imgname = imgname[:-3] + 'png'
        if os.path.exists(os.path.join(imgdir, imgname)):
            DAns['imgurl'] = '{}://{}/static/pdf_img/{}'.format(
                request.scheme, request.get_host(), imgname
            )

    DAns['citation_count'] = 0
    DAns.update(Get_Paper_Citation(paperid))
    DAns['abstract'] = ''
    Abs = Get_Paper_Abstract(paperid, cursor)
    if Abs:
        DAns.update(Abs)
    Author_Info = Get_Author_List(paperid, cursor)
    DAns['Authors'] = []
    for i, name in enumerate(Author_Info['author_name_list']):
        remote_id = Author_Info['author_id_list'][i]
        DAns['Authors'].append({
            'name': name, 'remote_id': remote_id,
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
