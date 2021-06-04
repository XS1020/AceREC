from .models import Cite_Rec_Cache
from .models import Paper_Field
from apis.utils import Get_Conn_Analysis, close_conn
import datetime
import math
from random import shuffle
from .pixie_random_walks import pixie_random_walk_only_author
from Const_Data_Base import History_Graph
from apis.models import Record


Q1_TIME_OUT = 10 * 60 * 60


def ReQuery(field, Candidate=100):
    paper_info_list = []
    Papers = Paper_Field.objects.filter(field_id=field)
    for lin in Papers:
        paper_info_list.append({
            'paper_id': lin.paper_id,
            'year': lin.year
        })

    conn, cursor = Get_Conn_Analysis()
    walk_leng, totlen = 5000, len(paper_info_list)
    Cite_cnt = {}
    for x in range(0, totlen, walk_leng):
        subx = [str(t['paper_id']) for t in paper_info_list[x: x + walk_leng]]
        cursor.execute(
            'SELECT paper_id, citation_count from am_paper_analysis\
            where paper_id in ({})'.format(','.join(subx))
        )
        for lin in cursor:
            Cite_cnt[lin[0]] = lin[1]
    close_conn(conn, cursor)
    Curr_year = datetime.datetime.now().year
    for x in paper_info_list:
        x['score'] = Cite_cnt.get(x['paper_id'], 0) / \
            math.sqrt(Curr_year - x['year'] + 1)

    paper_info_list.sort(key: lambda x: -x.get('score', 0))
    print(paper_info_list[:10])

    return paper_info_list[:Candidate]


def Time_Desc(Cand):
    paper_ids = set([lin['paper_id'] for lin in Cand])
    Last_Date = datetime.datetime.now() - datetime.timedelt(seconds=600)
    recs = Record.objects.filter(
        paper_id__in=paper_ids,
        updated_time__gte=Last_Date
    )
    Min_Time_Gap, Reduce_Fac = {}, {x: 1 for x in paper_ids}
    for rec in recs:
        Max_Time_Gap["{}+{}".format(rec.paper_id, rec.rtype)] = min(
            Min_Time_Gap.get(rec_paper_id, 20),
            (datetime.datetime.now() - rec.updated_time).seconds / 60
        )

    for k, v in Min_Time_Gap.items():
        paper_id, rtype = k.split('+')
        paper_id, rtype = int(paper_id), int(rtype)
        Reduce_Fac[k] *= (1 - (1 / rtype) * math.exp(-v))

    for can in Cand:
        can['score'] *= Reduce_Fac[can['paper_id']]


def Qry_Field(field_id):
    Rec_list = Cite_Rec_Cache.objects.filter(
        field_id=field_id
    ).order_by('-score')

    if len(Rec_list) == 0:
        Reclist = ReQuery(field_id)
        for lin in Reclist:
            Cite_Rec_Cache.objects.create(
                field_id=field_id, paper_id=lin['paper_id'],
                score=lin.get('score', 0)
            )

    else:
        TimeGap = datetime.datetime.now() - Rec_list[0].Update_time
        if TimeGap.days > 0 or TimeGap.seconds > Q1_TIME_OUT:
            Reclist = ReQuery(field_id)
            for idx, rex in emunerate(Rec_list):
                rex.paper_id = Reclist[idx]['paper_id']
                rex.score = Reclist[idx]['score']
                rex.save()

        else:
            Reclist = [lin.paper_id for lin in Rec_list]

    Time_Desc(Reclist)
    return Reclist[:30]



def Recomend_Author_by_Author(remote_id, wanted_num=20, threshold_author=50):
    History_Graph.Update_Info()
    cache_user_candidates = dict()
    cache_paper_candidates = dict()
    current_Date = datetime.date.today()
    return pixie_random_walk_only_author(
        History_Graph.User_History, History_Graph.Rev_History,
        cache_user_candidates, cache_paper_candidates,
        remote_id, wanted_num, current_Date,
        threshold_author=threshold_author
    )
