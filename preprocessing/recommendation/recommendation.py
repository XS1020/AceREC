import math
import json
import time
import torch
import pickle
import random
import numpy as np
from datetime import datetime
from pixie_random_walks import *

def recommend_author_by_author(userid, wanted_num=10, threshold_author=50):
    global user_history, record_paperid2uid, date
    cache_user_candidates = dict()
    cache_paper_candidates = dict()
    return pixie_random_walk_only_author(user_history, record_paperid2uid, cache_user_candidates, cache_paper_candidates, userid, wanted_num, date, threshold_author=threshold_author)

def recommend_paper_by_interest_and_citation(userid, max_num=30):
    global Author_field, Field_paper, paper_citation_year

    fields = list(Author_field[userid])
    random.shuffle(fields)
    papers = []
    currentYear = datetime.now().year
    for fieldid in fields[:3]:
        tmp_papers = [(paperid, paper_citation_year[paperid][0]/np.sqrt(currentYear-paper_citation_year[paperid][1]+1)) for paperid in Field_paper[fieldid]]
        tmp_papers = sorted(tmp_papers, key=lambda x: x[1], reverse=True)[:max_num]
        papers += tmp_papers
    random.shuffle(papers)
    return [paper[0] for paper in papers[:max_num]]

def recommend_paper_by_history(userid):
    global user_history, record_paperid2uid, date
    cache_user_candidates = dict()
    cache_paper_candidates = dict()
    return pixie_random_walk_only_paper(user_history, record_paperid2uid, cache_user_candidates, cache_paper_candidates, userid, 20, date)

def recommend_paper_by_paper(paperid, wanted_num=10, test=False):
    global paperid2com, communities, id2paperid, paperid2id, embeddings_all, tmpid2id_all, id2tmpid_all

    if test:
        time_0 = time.time()

    communityid = paperid2com[str(paperid)]
    community = communities[communityid]
    size = len(community)

    if test:
        print(size)

    if size < 20:
        community = [idx for idx in community if idx != paperid]
        random.shuffle(community)
        return community[:wanted_num]

    embeddings = embeddings_all[communityid]
    tmpid2id = tmpid2id_all[communityid]
    id2tmpid = id2tmpid_all[communityid]

    if test:
        time_1 = time.time()
        print("[INFO] First stage uses time:", time_1-time_0, "s")

    # distances = np.sum((embeddings - embeddings[id2tmpid[str(paperid2id[str(paperid)])]]) ** 2, axis=1)
    similarities = embeddings.dot(embeddings[id2tmpid[str(paperid2id[str(paperid)])]])

    if test:
        time_2 = time.time()
        print("[INFO] Second stage uses time:", time_2-time_1, "s")

    # result = sorted(enumerate(distances), key=lambda x: x[1])[1:wanted_num+1]
    similarities = torch.tensor(similarities)
    values, indices = similarities.topk(wanted_num+1, largest=True)

    if test:
        time_3 = time.time()
        print("[INFO] Third stage uses time:", time_3-time_2, "s")
        print("----------------------------")

    return [id2paperid[str(tmpid2id[str(paper.item())])] for paper in indices[1:]]
    # return [id2paperid[str(tmpid2id[str(paper[0])])] for paper in result]

def recommend_paper_by_achievements(userid, start_num=16, test=False):
    global author_info, paper_citation_year
    author = author_info[userid]
    papers = [(paperid, paper_citation_year[paperid][1]) for paperid in author['paper_id']]
    papers = sorted(papers, key=lambda x: x[1], reverse=True)[:6]
    candidate_papers = []
    for paper in papers[:6]:
        candidate_papers += recommend_paper_by_paper(paper[0], start_num, test=test)
        start_num = max(start_num//2, 2)
    random.shuffle(candidate_papers)
    return candidate_papers

def recommend_paper_by_user(userid, wanted_num=20, test=False):
    global author_info, user_history

    author = author_info[userid]
    published_papers = set(author['paper_id'])

    papers = []

    time0 = time.time()

    target_num = math.ceil(wanted_num * min(author['paper_count']*0.06, 0.6))
    papers_recommended_by_achievement = recommend_paper_by_achievements(userid)
    cnt = 0
    for paperid in papers_recommended_by_achievement:
        if paperid not in published_papers:
            papers.append(paperid)
            cnt += 1
            if cnt == target_num:
                break

    time1 = time.time()

    author_history_size = len(user_history[userid])
    # print(author_history_size)
    if author_history_size > 10:
        target_num = math.ceil((wanted_num-len(papers)) * min((author_history_size-5) * 0.1, 1))
        papers_recommended_by_history = recommend_paper_by_history(userid)
        print(papers_recommended_by_history)
        papers += [paper[0] for paper in papers_recommended_by_history[:target_num] if paper[0] not in published_papers]

    time2 = time.time()

    target_num = max(wanted_num - len(papers), 1)
    cnt = 0
    for paperid in recommend_paper_by_interest_and_citation(userid, max_num=wanted_num):
        if paperid not in published_papers:
            papers.append(paperid)
            cnt += 1
            if cnt == target_num:
                break

    time3 = time.time()

    papers = list(set(papers))
    random.shuffle(papers)

    time4 = time.time()
    if test:
        print(time1-time0, time2-time1, time3-time2, time4-time3)

    return papers[:wanted_num]

if __name__ == "__main__":

    with open("data/paperid2com.json", 'r') as f:
        paperid2com = json.load(f)
    with open("data/communities_final.json", 'r') as f:
        communities = json.load(f)
    with open("data/id2paperid.json", 'r') as f:
        id2paperid = json.load(f)
    with open("data/paperid2id.json", 'r') as f:
        paperid2id = json.load(f)
    with open("data/author_info.pickle", 'rb') as f:
        author_info = pickle.load(f)
    with open("data/paper_citation_year.pickle", 'rb') as f:
        paper_citation_year = pickle.load(f)
    with open("data/Paper_title.pickle", 'rb') as f:
        Paper_title = pickle.load(f)
    with open("data/Author_field.pickle", 'rb') as f:
        Author_field = pickle.load(f)
    with open("data/Field_paper.pickle", 'rb') as f:
        Field_paper = pickle.load(f)
    with open("data/history/user_history_date=119.pickle", 'rb') as f:
        user_history = pickle.load(f)
    with open("data/history/record_paperid2uid_data=119.pickle", 'rb') as f:
        record_paperid2uid = pickle.load(f)
    embeddings_all = dict()
    tmpid2id_all = dict()
    id2tmpid_all = dict()
    for communityid in communities:
        try:
            with open("node2vec/embeddings/"+communityid+".csv.pkl", 'rb') as f:
                embeddings_all[communityid] = pickle.load(f)
                embeddings_all[communityid] /= np.sqrt(np.sum(embeddings_all[communityid]**2, axis=1)).reshape(-1, 1)
            with open("node2vec/data/"+communityid+"_tmpid2id.json", 'r') as f:
                tmpid2id_all[communityid] = json.load(f)
            with open("node2vec/data/"+communityid+"_id2tmpid.json", 'r') as f:
                id2tmpid_all[communityid] = json.load(f)
        except:
            pass

    date = 120

    # pid = 348096325
    # papers = recommend_paper_by_paper(pid, 16)
    # for paper in papers:
    #     print(Paper_title[paper])
    # exit()

    authorids = [authorid for authorid in author_info.keys()]
    random.shuffle(authorids)
    authorid = authorids[0]
    authorid = 1000504663
    print("[INFO] 作者ID:", authorid)
    print("[INFO] 作者姓名:", author_info[authorid]['chinese_name'])
    print("[INFO] 研究领域:", author_info[authorid]['research_list'])

    recommend_paper = True
    if recommend_paper:
        author = author_info[authorid]
        papers = [(paperid, paper_citation_year[paperid][1]) for paperid in author['paper_id']]
        papers = sorted(papers, key=lambda x: x[1], reverse=True)[:6]
        for paper in papers[:6]:
            print(Paper_title[paper[0]])
        print("-----------------------------")

        start_time = time.time()

        papers = recommend_paper_by_user(authorid, test=True)

        end_time = time.time()
        print("[INFO] Use time:", end_time-start_time, "s")

        for idx, paperid in enumerate(papers):
            print(str(idx+1)+".", Paper_title[paperid])
    else:
        if len(author_info[authorid]['paper_id']) <= 10:
            exit("这个用户阅读量太少")
        time0 = time.time()
        authors = recommend_author_by_author(authorid, wanted_num=20, threshold_author=20)
        time1 = time.time()
        print("[INFO] Use time:", time1-time0, "s")
        for author in authors:
            print(author[1], author_info[author[0]]['id'], author_info[author[0]]['chinese_name'], author_info[author[0]]['research_list'])
