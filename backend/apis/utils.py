import MySQLdb
import MySQLdb.cursors
import datetime
import json
from User.models import User_Info
from collections import Iterable


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


def Get_Conn_Analysis():
    num = 0
    while True:
        num += 1
        try:
            conn = MySQLdb.connect(
                host='server.acemap.cn', port=13307,
                charset='utf8mb4', user='remote',
                passwd='bJuPOIQn9LuNZqmFR9qa', db='am_analysis',
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

    if len(Ans) == 0:
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
        conn, cursor = Get_Conn_Paper()
        Flag = True

    cursor.execute(
        'SELECT paper_id, doi from am_paper\
        where paper_id = {}'.format(paperid)
    )
    Ans = cursor.fetchone()
    if Flag:
        close_conn(conn, cursor)
    return None if not Ans else {'doi': Ans[1]}


def Get_Paper_Ref(paperid, cursor=None):
    Flag = False
    if cursor is None:
        (conn, cursor), Flag = Get_Conn_Paper(), True

    cursor.execute(
        'SELECT paper_id, reference_id from \
        am_paper_reference where paper_id = {}'.format(paperid)
    )

    Reflist = [x[1] for x in cursor]

    if Flag:
        close_conn(conn, cursor)

    return None if Reflist == [] else {'Ref': Reflist}


def Get_Citation_Trend(paperid, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Analysis()
        Flag = True

    cursor.execute(
        'SELECT citation_trend from am_paper_analysis \
        where paper_id = {}'.format(paperid)
    )

    ctrend = cursor.fetchone()

    if Flag:
        close_conn(conn, cursor)
    return [] if not ctrend else json.loads(ctrend[0])


def Get_Paper_Keyword(
    paperid, wordname='keyword',
    levelname='level', cursor=None
):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True

    cursor.execute(
        'SELECT am_field.`name`, taf.field_id, am_field.`level` from (\
         SELECT paper_id, field_id FROM am_paper_field WHERE paper_id = {}\
        ) as taf JOIN am_field on am_field.field_id = taf.field_id'.format(paperid)
    )

    Keywords = []
    for lin in cursor:
        Keywords.append({wordname: lin[0], levelname: lin[2]})

    if Flag:
        close_conn(conn, cursor)

    return Keywords


def Remote_to_Local(remote_ids):
    if isinstance(remote_ids, Iterable):
        Ans = {x: -1 for x in remote_ids}
        auser = User_Info.objects.filter(remote_id__in=list(remote_ids))
        for lin in auser:
            Ans[lin.remote_id] = lin.local_id
    else:
        auser = User_Info.objects.filter(remote_id=remote_ids)
        Ans = -1 if len(auser) < 1 else auser[0].local_id
    return Ans


def Local_to_Remote(Local_ids):
    if isinstance(Local_ids, Iterable):
        Ans = {x: -1 for x in Local_ids}
        auser = User_Info.objects.filter(local_id__in=list(Local_ids))
        for lin in auser:
            Ans[lin.local_id] = lin.remote_id
    else:
        auser = User_Info.objects.filter(local_id=Local_ids)
        Ans = -1 if len(auser) < 1 else auser[0].remote_id
    return Ans


def Get_Person_Cite(person_id):
    conn, cursor = Get_Conn_Paper()

    cursor.execute(
        'SELECT paper_id from am_paper_author\
        where author_id = {}'.format(person_id)
    )

    Paperlist = []
    for lin in cursor:
        Paperlist.append(lin[0])

    close_conn(conn, cursor)

    conn, cursor = Get_Conn_Analysis()

    cursor.execute(
        'SELECT citation_trend from am_paper_analysis\
        where paper_id in ({})'.format(','.join(str(x) for x in Paperlist))
    )
    Cite_tot = {}
    for lin in cursor:
        INFO = json.loads(lin[0])
        for cite_cnt in INFO:
            year, cnt = cite_cnt['year'], cite_cnt['citation_count']
            Cite_tot[year] = Cite_tot.get(year, 0) + cnt

    close_conn(conn, cursor)
    Ans = []
    for k, v in Cite_tot.items():
        Ans.append({
            'citation_count': v,
            'year': k
        })
    return Ans


def Get_Related_Authors(author_id, cursor=None):
    Flag = False
    if cursor is None:
        conn, cursor = Get_Conn_Paper()
        Flag = True

    cursor.execute(
        'SELECT am_paper_author.author_id from (\
            SELECT paper_id, year FROM am_paper WHERE paper_id in (\
                SELECT paper_id FROM am_paper_author WHERE author_id = {}\
            ) ORDER BY `year` DESC LIMIT 10\
        ) as taf JOIN am_paper_author ON \
        taf.paper_id = am_paper_author.paper_id'.format(author_id)
    )

    Count = {}
    for lin in cursor:
        Count[lin[0]] = Count.get(lin[0], 0) + 1

    if Flag:
        close_conn(conn, cursor)

    return Count


def Get_Person_Cite_Count(personid):
    conn, cursor = Get_Conn_Analysis()
    cursor.execute(
        'SELECT citation_count, paper_count, hindex from\
        am_author_analysis where author_id = {}'.format(personid)
    )
    Ans = cursor.fetchone()
    close_conn(conn, cursor)
    return Ans
