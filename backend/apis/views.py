from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
import MySQLdb
import MySQLdb.cursors


# Create your views here.

def Get_Conn_Paper():
    num = 0
    while True:
        num += 1
        try:
            conn = MySQLdb.connect(
                host='server.acemap.cn', port=13307,
                charset='utf8mb4', user='remote',
                passwd='bJuPOIQn9LuNZqmFR9qa', db='am_paper',
                cursorclass=MySQLdb.cursors.SSCursor
            )
        except Exception as err:
            print(
                datetime.datetime.now(),
                "{}. Retry for {} times".format(err, num)
            )
        else:
            break
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    try:
        cursor.close()
    except Exception as err:
        print(datetime.datetime.now(), "cursor close failed", err)
    try:
        conn.close()
    except Exception as err:
        print(datetime.datetime.now(), "connection close failed", err)


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


def Main_Page_Card_Info(request):
    Data = request.GET

    # Error Part
    if not Data:
        HttpResponseBadRequest('No \"paperid\" Found')
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
        dRes['year'], dRes['title'] = lin[0], lin[1]
        jourid, confind, IsLine = lin[2], lin[3], True

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

    if not IsLine:
        close_conn(conn, cursor)
        return HttpResponseBadRequest('No Such Paper')

    close_conn(conn, cursor)

    return JsonResponse(dRes)
