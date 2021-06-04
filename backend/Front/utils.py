import json
from .models import Cite_Rec_Cache
from .models import Paper_Field, Sim_Rec_Cache
from apis.utils import Get_Conn_Analysis, close_conn
import datetime
import math
from random import shuffle
from .pixie_random_walks import pixie_random_walk_only_author
from .pixie_random_walks import pixie_random_walk_only_paper
from Const_Data_Base import History_Graph
from apis.models import Record
from .models import Recom_Data, Embeddings
import torch
from tqdm import tqdm
from Const_Var import Cheat_Embeddings, PaperId2Pos, PaperPos2Id
from Const_Var import Field_List

import time
from User.models import User_Papers, User_Interest


Q1_TIME_OUT = 5 * 60 * 60
Q2_TIME_OUT = 10 * 60 * 60


def ReQuery(field, Candidate=50):
    paper_info_list = []
    # Papers = Paper_Field.objects.filter(field_id=field)
    Papers = Paper_Field.objects.raw(
        'SELECT * from front_paper_field where field_id = %s\
        order by cite_cnt desc limit 10000', [field]
    )
    Curr_year = datetime.datetime.now().year
    for lin in Papers:
        paper_info_list.append({
            'paper_id': lin.paper_id, 'year': lin.year,
            'score': lin.cite_cnt / math.sqrt(Curr_year - lin.year + 1)
        })

    paper_info_list.sort(key=lambda x: -x.get('score', 0))
    return paper_info_list[:Candidate]


def Time_Desc(Cand):
    paper_ids = set([lin['paper_id'] for lin in Cand])
    Last_Date = datetime.datetime.now() - datetime.timedelta(seconds=6000)
    recs = Record.objects.filter(
        paper_id__in=paper_ids,
        updated_time__gte=Last_Date
    )
    Min_Time_Gap, Reduce_Fac = {}, {x: 1 for x in paper_ids}
    for rec in recs:
        Min_Time_Gap["{}+{}".format(rec.paper_id, rec.rtype)] = min(
            Min_Time_Gap.get(rec.paper_id, 20),
            (datetime.datetime.now() - rec.updated_time).seconds / 600
        )

    for k, v in Min_Time_Gap.items():
        paper_id, rtype = k.split('+')
        paper_id, rtype = int(paper_id), int(rtype)
        Reduce_Fac[paper_id] *= (1 - (1 / rtype) * math.exp(-v))

    for can in Cand:
        can['score'] *= Reduce_Fac[can['paper_id']]


def Qry_Field(field_id, Number=10):
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
    Reclist.sort(key=lambda x: -x['score'])
    return Reclist[:Number]


def Qry_Sim_of_Paper(paper_id, Candidate=50):
    ocluster = Recom_Data.objects.filter(paper_id=paper_id)
    if len(ocluster) == 0:
        return []
    bel = ocluster[0].belong
    pos2pid, pid2pos = {}, {}

    Embeds = Cheat_Embeddings.get(bel, [])
    if len(Embeds) == 0:
        return []

    pid2pos = PaperId2Pos[bel]
    pos2pid = PaperPos2Id[bel]

    """
    Embeds, Idx = [], 0
    Emb_clu = Embeddings.objects.filter(belong=bel)
    for x in tqdm(Emb_clu):
        Embeds.append(json.loads(x.Embedding))
        pid2pos[x.paper_id], pos2pid[Idx] = Idx, x.paper_id
        Idx += 1
    if len(Embeds) == 0:
        return []
    Embeds = torch.tensor(Embeds)
    """

    self_Emb = Embeds[pid2pos[paper_id]]
    Similarity = torch.sum(Embeds * self_Emb, dim=1)
    Ans = Similarity.topk(Candidate + 1, largest=True)
    Indexes = Ans.indices.to('cpu').detach().tolist()
    Vals = Ans.values.to('cpu').detach().tolist()
    Repo = []
    if len(Indexes) > 1:
        for i in range(1, len(Indexes)):
            Repo.append({
                'paper_id': pos2pid[Indexes[i]],
                'score': Vals[i]
            })
    return Repo


def Recommend_paper_by_Sim(paper_id, wanted_num=10):
    Cache_info = Sim_Rec_Cache.objects.filter(
        paper_id=paper_id
    ).order_by('-Sim')
    Flag = False
    if len(Cache_info) < wanted_num * 2:
        Flag = True
    else:
        TimeGap = datetime.datetime.now() - Cache_info[0].update_time
        if TimeGap.days > 0 or TimeGap.seconds > Q2_TIME_OUT:
            Flag = True
    if Flag:
        Rec_list = Qry_Sim_of_Paper(paper_id, max(50, wanted_num * 2))
        Cache_info.delete()
        for Rec in Rec_list:
            Sim_Rec_Cache.objects.create(
                paper_id=paper_id,
                rec_id=Rec['paper_id'],
                Sim=Rec['score']
            )

    else:
        Rec_list = [{
            'paper_id': x.rec_id,
            'score': x.Sim
        } for x in Cache_info]

    Time_Desc(Rec_list)
    Rec_list.sort(key=lambda x: -x['score'])
    return Rec_list[:wanted_num]


def Recommend_paper_by_paper(paper_id, wanted_num):
    Sim_rec = Recommend_paper_by_Sim(paper_id, wanted_num)
    Exact_part = []
    if len(Sim_rec) < wanted_num:
        ocluster = Recom_Data.objects.filter(paper_id=paper_id)
        if len(ocluster) != 0:
            bel = ocluster[0].belong
            objs = Recom_Data.objects.filter(belong=bel)
            pps = [x.paper_id for x in objs]
            shuffle(pps)
            Exact_part = pps[: wanted_num - len(Sim_rec)]

    Ready = set([x['paper_id'] for x in Sim_rec] + Exact_part)
    if paper_id in Ready:
        Ready.remove(paper_id)
    return list(Ready)


def Get_top_six(remote_id):
    objs = User_Papers.objects.filter(remote_id=remote_id)
    paper_id_list = [x.paper_id for x in objs]
    if len(paper_id_list) == 0:
        return []

    conn, cursor = Get_Conn_Analysis()
    cursor.execute(
        'SELECT paper_id, citation_count from\
        am_paper_analysis where paper_id in ({})\
        order by citation_count desc'.format(
            ','.join(str(x) for x in paper_id_list)
        )
    )
    topsix = []
    for lin in cursor:
        topsix.append(lin[0])
        if len(topsix) == 6:
            break
    close_conn(conn, cursor)

    return topsix


def Recommend_paper_by_Achieve(remote_id, start=64):
    topsix = Get_top_six(remote_id)
    Candidate = []
    for x in topsix:
        Candidate += Recommend_paper_by_Sim(x, start)
        start = max(start // 2, 4)
    Candidate = list(set(x['paper_id'] for x in Candidate))
    shuffle(Candidate)
    return Candidate


def recomemd_paper_by_interest(local_id, max_num=30):
    objs = User_Interest.objects.filter(local_id=local_id)
    interest_list = [x.interest_field for x in objs]
    if interest_list == []:
        shuffle(Field_List)
        interest_list = Field_List[:2]
    else:
        shuffle(interest_list)
        interest_list = interest_list[:3]

    # print("List", interest_list)

    Qrynum = math.ceil(max_num / 3)
    Ans = []
    for x in interest_list:
        # t1 = time.time()
        Ans += Qry_Field(x, Qrynum)
        # print(x, time.time() - t1)

    Ans = list(set(x['paper_id'] for x in Ans))
    shuffle(Ans)
    return Ans[:max_num]


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


def Rec_paper_by_His(remote_id):
    cache_user_candidates = dict()
    cache_paper_candidates = dict()
    current_Date = datetime.date.today()
    return pixie_random_walk_only_paper(
        History_Graph.User_History, History_Graph.Rev_History,
        cache_user_candidates, cache_paper_candidates,
        remote_id, 20, current_Date
    )


def Rec_by_User(local_id, remote_id, wanted_num=20):
    debug = False
    History_Graph.Update_Info()

    if debug:
        Start_time = time.time()

    papers = User_Papers.objects.filter(remote_id=remote_id)
    paperset = set(x.paper_id for x in papers)
    paper_cnt, owanted = len(paperset), wanted_num

    if debug:
        time1 = time.time()
        print("T1:", time1 - Start_time)

    target_num = math.ceil(wanted_num * min(paper_cnt * 0.06, 0.6))
    paper_rec1 = Recommend_paper_by_Achieve(
        remote_id
    ) if remote_id >= 0 else []
    paper_rec1 = list(set(paper_rec1) - paperset)[:target_num]

    if debug:
        time2 = time.time()
        print("T2:", time2 - time1)

    His_Size = len(History_Graph.User_History.get(remote_id, []))
    paperrec2 = []
    wanted_num -= len(paper_rec1)

    if debug:
        print(His_Size)

    if His_Size > 10:
        target_num = math.ceil(wanted_num * min((His_Size - 5) * 0.1, 1))
        paperrec2 = Rec_paper_by_His(remote_id)
        paperrec2 = [x[0] for x in paperrec2]
        paperrec2 = list(set(paperrec2) - paperset)

    if debug:
        time3 = time.time()
        print("T3:", time3 - time2)

    wanted_num -= len(paperrec2)
    wanted_num = max(wanted_num, 1)
    paperrec3 = recomemd_paper_by_interest(local_id, owanted)
    paperrec3 = list(set(paperrec3) - paperset)

    if debug:
        time4 = time.time()
        print("T4:", time4 - time3)

    paper_all = list(set(paper_rec1 + paperrec2 + paperrec3))
    shuffle(paper_all)
    return paper_all[:owanted]
