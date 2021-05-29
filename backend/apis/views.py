from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import os
from Const_Var import Paper_Pdf_Mapping
from backend.settings import STATICFILES_DIRS
import MySQLdb
import MySQLdb.cursors
import datetime
from .utils import Get_Conn_Paper
from .utils import Get_Conn_Analysis
from .utils import close_conn

# Create your views here.


def Get_Paper_Conf(confid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True

    cursor.execute(
        'SELECT name, abbreviation from am_conference_series \
        where conference_series_id = {}'.format(confid)
    )
    Ans = cursor.fetchone()
    if Flag:
        close_conn(conn, cursor)
    return None if not Ans else {'conference': Ans[0], 'Abbr': Ans[1]}


def Get_Paper_Jour(confid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True

    cursor.execute(
        'SELECT name from am_journal \
        where journal_id = {}'.format(confid)
    )
    Ans = cursor.fetchone()
    if Flag:
        close_conn(conn, cursor)
    return None if not Ans else {'conference': Ans[0]}


def Get_Author_List(paperid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True

    cursor.execute(
        'SELECT tau.aid, am_author.`name` from (\
            SELECT author_id as aid, sequence as seq \
            from am_paper_author where paper_id = {}\
        ) as tau \
        join am_author on am_author.author_id = tau.aid\
        order by tau.seq'.format(paperid)
    )
    Aus = {
        'author_name_list': [],
        'author_id_list': []
    }
    for lin in cursor:
        Aus['author_name_list'].append(lin[1])
        Aus['author_id_list'].append(lin[0])
    if Flag:
        close_conn(conn, cursor)
    return Aus


def Get_Paper_Abstract(paperid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True
    cursor.execute(
        'SELECT abstract from am_paper_abstract \
        where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchone()
    if Flag:
        close_conn(conn, cursor)
    return None if not Ans else {'abstract': Ans[0]}


def Get_Paper_Citation(paperid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Analysis()
        Flag = True
    cursor.execute(
        'SELECT citation_count from am_paper_analysis \
         where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchone()

    if Flag:
        close_conn(conn, cursor)
    return {'citation_count': 0 if not Ans else Ans[0]}


def Get_Org_Url(paperid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True
    cursor.execute(
        'SELECT paper_id, type, source_url from am_paper_url \
         where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchall()

    if Flag:
        close_conn(conn, cursor)

    if Ans == []:
        return {'url': ''}
    Ansline = 0
    for lin in range(len(Ans)):
        if Ans[lin][1] == 1:
            Ansline = lin
            break
        elif Ans[lin][1] < Ans[Ansline][1]:
            Ansline = lin
    return {'url': Ans[Ansline][2]}


def Get_Paper_Doi(paperid, cursor=None):
    Flag = False
    if cursor is None:
        cursor, conn = Get_Conn_Paper()
    cursor.execute(
        'SELECT paper_id, doi from am_paper\
        where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchone()
    if Flag:
        close_conn(conn, cursor)
    return None if not Ans else {'doi': Ans[1]}


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
        return HttpResponseBadRequest('Not Int Paperid')

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
        return HttpResponseBadRequest('Not a Int Paperid')

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
    Data = request.GET

    if not Data or 'userid' not in Data or 'paperid' not in Data:
        return HttpResponseBadRequest("No Sufficient Data")

    

