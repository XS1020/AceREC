import math
import json
import time
import kdtree
import pickle
import random
import numpy as np
from tqdm import tqdm
from datetime import datetime

def recommend_author_by_author(userid, wanted_num=10):
    return []

def recommend_paper_by_interest_and_citation(userid, max_num=20):
    global Author_field, paper_citation_year, citation_time_rank_by_fieldid

    fields = list(Author_field[userid])
    random.shuffle(fields)
    papers = []
    for fieldid in fields[:3]:
        papers += citation_time_rank_by_fieldid[fieldid][:max_num]
    random.shuffle(papers)
    return papers[:max_num]

def recommend_paper_by_history(userid):
    return []

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

    distances = np.sum((embeddings - embeddings[id2tmpid[str(paperid2id[str(paperid)])]]) ** 2, axis=1)

    if test:
        time_2 = time.time()
        print("[INFO] Second stage uses time:", time_2-time_1, "s")

    result = sorted(enumerate(distances), key=lambda x: x[1])[1:wanted_num+1]

    if test:
        time_3 = time.time()
        print("[INFO] Third stage uses time:", time_3-time_2, "s")
        print("----------------------------")

    return [id2paperid[str(tmpid2id[str(paper[0])])] for paper in result]

def recommend_paper_by_paper_fast(paperid, wanted_num=10, test=False):
    global paperid2com, communities, paperid2neighbors

    communityid = paperid2com[str(paperid)]
    community = communities[communityid]

    if len(community) < 20:
        community = [idx for idx in community if idx != paperid]
        random.shuffle(community)
        return community[:wanted_num]

    return paperid2neighbors[paperid][:wanted_num]

def recommend_paper_by_achievements(userid, start_num=64, test=False):
    global author_info, paper_citation_year, paperid2neighbors
    author = author_info[userid]
    papers = [(paperid, paper_citation_year[paperid][1]) for paperid in author['paper_id']]
    papers = sorted(papers, key=lambda x: x[1], reverse=True)[:6]
    candidate_papers = []
    for paper in papers[:6]:
        # candidate_papers += recommend_paper_by_paper(paper[0], start_num)
        candidate_papers += recommend_paper_by_paper_fast(paper[0], start_num)
        start_num = max(start_num//2, 4)
    random.shuffle(candidate_papers)
    return candidate_papers

def recommend_paper_by_user(userid, wanted_num=20, test=False):
    global author_info

    papers = []

    time0 = time.time()
    target_num = math.ceil(wanted_num * min(author_info[userid]['paper_count']*0.06, 0.6))
    papers_recommended_by_achievement = recommend_paper_by_achievements(userid)
    papers += papers_recommended_by_achievement[:target_num]

    time1 = time.time()
    author_history_size = 0
    if author_history_size > 10:
        target_num = math.ceil((wanted_num-len(papers)) * min((author_history_size-5) * 0.1, 1))
        papers_recommended_by_history = recommend_paper_by_history(userid)
        papers += papers_recommended_by_history[:target_num]

    time2 = time.time()
    target_num = max(wanted_num - len(papers), 1)
    papers_recommended_by_interest_and_citation = recommend_paper_by_interest_and_citation(userid, max_num=wanted_num)
    papers += papers_recommended_by_interest_and_citation[:target_num]

    time3 = time.time()
    papers = list(set(papers))
    random.shuffle(papers)

    time4 = time.time()
    if test:
        print(time4-time3, time3-time2, time2-time1, time1-time0)

    return papers[:wanted_num]

if __name__ == "__main__":

    print("[INFO] Load in data...")
    with open("data/paperid2com.json", 'r') as f:
        paperid2com = json.load(f)
    with open("data/communities_final.json", 'r') as f:
        communities = json.load(f)
    # with open("data/id2paperid.json", 'r') as f:
    #     id2paperid = json.load(f)
    # with open("data/paperid2id.json", 'r') as f:
    #     paperid2id = json.load(f)
    with open("data/author_info.pickle", 'rb') as f:
        author_info = pickle.load(f)
    with open("data/paper_citation_year.pickle", 'rb') as f:
        paper_citation_year = pickle.load(f)
    # with open("data/Paper_title.pickle", 'rb') as f:
    #     Paper_title = pickle.load(f)
    with open("data/Author_field.pickle", 'rb') as f:
        Author_field = pickle.load(f)
    # with open("data/Field_paper.pickle", 'rb') as f:
    #     Field_paper = pickle.load(f)
    with open("data/citation_time_rank_by_fieldid.pickle", 'rb') as f:
        citation_time_rank_by_fieldid = pickle.load(f)
    with open("data/paperid2neighbors.pickle", 'rb') as f:
        paperid2neighbors = pickle.load(f)
    # embeddings_all = dict()
    # tmpid2id_all = dict()
    # id2tmpid_all = dict()
    # for communityid in communities:
    #     try:
    #         with open("node2vec/embeddings/"+communityid+".csv.pkl", 'rb') as f:
    #             embeddings_all[communityid] = pickle.load(f)
    #         with open("node2vec/data/"+communityid+"_tmpid2id.json", 'r') as f:
    #             tmpid2id_all[communityid] = json.load(f)
    #         with open("node2vec/data/"+communityid+"_id2tmpid.json", 'r') as f:
    #             id2tmpid_all[communityid] = json.load(f)
    #     except:
    #         pass

    print("[INFO] Simulating...")
    user_character = dict()
    user_history = dict()
    for author_id in author_info:
        user_character[author_id] = random.random()
        user_history[author_id] = []

    for date in range(60):
        bar = tqdm(author_info)
        bar.set_description(f"Current data is {date}. ")
        for author_id in bar:
            if random.random() > user_character[author_id]:
                continue
            papers = recommend_paper_by_user(author_id, wanted_num=50, test=False)[:random.randint(1, 5)]
            for paperid in papers:
                user_history[author_id].append((paperid, date))

    with open("data/user_character.pickle", 'wb') as f:
        pickle.dump(user_character, f)
    with open("data/user_history.pickle", 'wb') as f:
        pickle.dump(user_history, f)
