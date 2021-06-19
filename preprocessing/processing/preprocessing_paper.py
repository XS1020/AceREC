import json
import time
import pickle
import random
import numpy as np
from tqdm import tqdm

def recommend_by_paper(paperid, wanted_num=10, test=False):
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

    distance = np.sum((embeddings - embeddings[id2tmpid[str(paperid2id[str(paperid)])]]) ** 2, axis=1)

    if test:
        time_2 = time.time()
        print("[INFO] Second stage uses time:", time_2-time_1, "s")

    result = sorted(enumerate(distance), key=lambda x: x[1])[1:wanted_num+1]

    if test:
        time_3 = time.time()
        print("[INFO] Third stage uses time:", time_3-time_2, "s")
        print("----------------------------")

    return [id2paperid[str(tmpid2id[str(paper[0])])] for paper in result]

if __name__ == "__main__":
    with open("data/paperid2com.json", 'r') as f:
        paperid2com = json.load(f)
    with open("data/communities_final.json", 'r') as f:
        communities = json.load(f)
    with open("data/id2paperid.json", 'r') as f:
        id2paperid = json.load(f)
    with open("data/paperid2id.json", 'r') as f:
        paperid2id = json.load(f)
    embeddings_all = dict()
    tmpid2id_all = dict()
    id2tmpid_all = dict()
    for communityid in communities:
        try:
            with open("node2vec/embeddings/"+communityid+".csv.pkl", 'rb') as f:
                embeddings_all[communityid] = pickle.load(f)
            with open("node2vec/data/"+communityid+"_tmpid2id.json", 'r') as f:
                tmpid2id_all[communityid] = json.load(f)
            with open("node2vec/data/"+communityid+"_id2tmpid.json", 'r') as f:
                id2tmpid_all[communityid] = json.load(f)
        except:
            pass

    paperid2neighbors = dict()
    for paperid in tqdm(paperid2com):
        paperid2neighbors[paperid] = recommend_by_paper(paperid, 64)
    print(paperid2neighbors)
    with open("data/paperid2neighbors.json", "w"):
        json.dump(paperid2neighbors, j)
