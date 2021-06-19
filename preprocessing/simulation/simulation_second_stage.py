import math
import json
import time
import pickle
import random
import numpy as np
from tqdm import tqdm
from datetime import datetime
from pixie_random_walks import *

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
    global user_history, record_paperid2uid, cache_user_candidates, cache_paper_candidates, date
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

def recommend_paper_by_user(userid, wanted_num=20):
    global author_info, user_history

    papers = []

    target_num = math.ceil(wanted_num * min(author_info[userid]['paper_count']*0.06, 0.6))
    papers_recommended_by_achievement = recommend_paper_by_achievements(userid)
    papers += papers_recommended_by_achievement[:target_num]

    author_history_size = len(user_history[userid])
    if author_history_size > 10:
        target_num = math.ceil((wanted_num-len(papers)) * min((author_history_size-5) * 0.1, 1))
        papers_recommended_by_history = recommend_paper_by_history(userid)
        papers += [paper[0] for paper in papers_recommended_by_history[:target_num]]

    target_num = max(wanted_num - len(papers), 1)
    papers_recommended_by_interest_and_citation = recommend_paper_by_interest_and_citation(userid, max_num=wanted_num)
    papers += papers_recommended_by_interest_and_citation[:target_num]

    papers = list(set(papers))
    random.shuffle(papers)

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
    with open("data/user_character.pickle", 'rb') as f:
        user_character = pickle.load(f)
    with open("data/user_history.pickle", 'rb') as f:
        user_history = pickle.load(f)
    with open("data/record_paperid2uid.pickle", 'rb') as f:
        record_paperid2uid = pickle.load(f)
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

    for date in range(60, 120):
        bar = tqdm(author_info)
        bar.set_description(f"Current date is {date}. Simulate visiting: ")
        cache_user_candidates = dict()
        cache_paper_candidates = dict()
        new_user_history = dict()
        for author_id in bar:
            if random.random() > user_character[author_id]:
                new_user_history[author_id] = []
                continue
            papers = recommend_paper_by_user(author_id, wanted_num=50)[:random.randint(1, 5)]
            new_user_history[author_id] = [(paperid, date) for paperid in papers]
        bar = tqdm(author_info)
        bar.set_description(f"Current date is {date}. Delete outdate data in user_history:")
        for author_id in bar:
            start = 0
            for paper in user_history[author_id]:
                if paper[1] > date - 60:
                    break
                start += 1
            user_history[author_id] = user_history[author_id][start:]
        bar = tqdm(record_paperid2uid)
        bar.set_description(f"Current date is {date}. Delete outdate data in record_paperid2uid:")
        for paperid in bar:
            start = 0
            for visiter in record_paperid2uid[paperid]:
                if visiter[1] > date - 60:
                    break
                start += 1
            record_paperid2uid[paperid] = record_paperid2uid[paperid][start:]
        bar = tqdm(new_user_history)
        bar.set_description(f"Current date is {date}. Add in new data:")
        for author_id in bar:
            if author_id not in user_history:
                user_history[author_id] = new_user_history[author_id]
            else:
                user_history[author_id] += new_user_history[author_id]
            for paper in new_user_history[author_id]:
                if paper[0] not in record_paperid2uid:
                    record_paperid2uid[paper[0]] = [(author_id, paper[1])]
                else:
                    record_paperid2uid[paper[0]].append((author_id, paper[1]))

        with open("data/history/user_history_date="+str(date)+".pickle", 'wb') as f:
            pickle.dump(user_history, f)
        with open("data/history/record_paperid2uid_data="+str(date)+".pickle", 'wb') as f:
            pickle.dump(record_paperid2uid, f)
