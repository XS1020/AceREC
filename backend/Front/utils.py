import json
from .models import Cite_Rec_Cache
from .models import Paper_Field
from apis.utils import Get_Conn_Analysis, close_conn
import datetime
import math
from random import shuffle
from .pixie_random_walks import pixie_random_walk_only_author
from Const_Data_Base import History_Graph
from apis.models import Record
from .models import Recom_Data, Embeddings
import torch


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

    paper_info_list.sort(key=lambda x: -x.get('score', 0))
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
            Rec_list.delete()
            for lin in Reclist:
                Cite_Rec_Cache.objects.create(
                    field_id=field_id, paper_id=lin['paper_id'],
                    score=lin.get('score', 0)
                )
        else:
            Reclist = [{
                'paper_id': lin.paper_id,
                'score': lin.score
            } for lin in Rec_list]

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


def Qry_Dist_of_Paper(paper_id, Candidate=100):
    ocluster = Recom_Data.objects.filter(paper_id=paper_id)
    if len(ocluster) == 0:
        return []
    bel = ocluster[0].belong
    cluster = Recom_Data.objects.filter(belong=bel)
    paper_id_list = [x.paper_id for x in cluster]
    pos2pid, pid2pos = {}, {}

    Embeds, Idx = [], 0
    Emb_clu = Embeddings.objects.filter(paper_id__in=paper_id_list)
    for x in Emb_clu:
        Embeds.append(json.loads(x.Embedding))
        pid2pos[x.paper_id], pid2pos[Idx] = Idx, x.paper_id
        Idx += 1
    if len(Embeds) == 0:
        return []
    device = torch.device('cuda:0' if torch.cuda.is_available else 'cpu')
    Embeds = torch.tensor(Embeds).to(device)
    self_Emb = Embeds[pid2pos[paper_id]]
    Similarity = torch.sum(Embeds * self_Emb, dim=1)
    Ans = Similarity.topk(Candidate + 1, largest=True).to('cpu')
    Indexes = Ans.indices.to('cpu').detach().tolist()
    Vals = Ans.values.to('cpu').detach().tolist()
    Repo = []
    if len(Indexes) > 1:
        for i in range(1, len(Indexes)):
            Repo.append({
                'paper_id': pos2pid[Indexes[i]],
                'Sim': Vals[i]
            })

    return Repo
