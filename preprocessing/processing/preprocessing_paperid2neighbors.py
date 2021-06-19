import os
import json
import time
import pickle
import random
import numpy as np
from tqdm import tqdm
from datetime import datetime
from sklearn import neighbors

if __name__ == "__main__":

    with open("data/paperid2com.json", 'r') as f:
        paperid2com = json.load(f)
    with open("data/communities_final.json", 'r') as f:
        communities = json.load(f)
    with open("data/id2paperid.json", 'r') as f:
        id2paperid = json.load(f)
    with open("data/paperid2id.json", 'r') as f:
        paperid2id = json.load(f)
    # with open("data/author_info.pickle", 'rb') as f:
    #     author_info = pickle.load(f)
    # with open("data/paper_citation_year.pickle", 'rb') as f:
    #     paper_citation_year = pickle.load(f)
    # with open("data/Paper_title.pickle", 'rb') as f:
    #     Paper_title = pickle.load(f)
    # with open("data/Author_field.pickle", 'rb') as f:
    #     Author_field = pickle.load(f)
    # with open("data/Field_paper.pickle", 'rb') as f:
    #     Field_paper = pickle.load(f)
    # with open("data/citation_time_rank_by_fieldid.pickle", 'rb') as f:
    #     citation_time_rank_by_fieldid = pickle.load(f)
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
    if os.path.exists("data/paperid2neighbors.pickle"):
        with open("data/paperid2neighbors.pickle", 'rb') as f:
            paperid2neighbors = pickle.load(f)

    for i, communityid in enumerate(embeddings_all):

        print(i)

        embeddings = embeddings_all[communityid]
        tmpid2id = tmpid2id_all[communityid]

        tmp_paperid = id2paperid[str(tmpid2id["0"])]
        if tmp_paperid in paperid2neighbors:
            continue

        flag = False
        if embeddings.shape[0] >= 20000:
            tree = neighbors.BallTree(embeddings)
            flag = True

        for tmpid in tqdm(range(embeddings.shape[0])):
            paperid = id2paperid[str(tmpid2id[str(tmpid)])]
            # if paperid in paperid2neighbors:
            #     continue
            if flag:
                distances, result = tree.query(embeddings[tmpid].reshape(1, -1), k=65)
                paperid2neighbors[paperid] = [id2paperid[str(tmpid2id[str(tmpid)])] for tmpid in result[0][1:]]
            else:
                distances = np.sum((embeddings - embeddings[tmpid]) ** 2, axis=1)
                result = sorted(enumerate(distances), key=lambda x: x[1])[1:65]
                paperid2neighbors[paperid] = [id2paperid[str(tmpid2id[str(paper[0])])] for paper in result]

        with open("data/paperid2neighbors.pickle", 'wb') as f:
            pickle.dump(paperid2neighbors, f)
