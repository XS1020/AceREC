import MySQLdb
import MySQLdb.cursors
import datetime
import json


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
    levelname='level',cursor=None
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


