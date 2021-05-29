import MySQLdb
import MySQLdb.cursors
import datetime


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