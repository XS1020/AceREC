import json
import pickle
import numpy as np
import pandas as pd

if __name__ == "__main__":
    # path = "data/edges.npy"
    #
    # data = np.load(path)
    # print(data)

    # with open("data/communities.json", 'r') as f:
    #     communities = json.load(f)
    #
    # cnt = 0
    # for key in communities:
    #     if len(communities[key]) >= 20:
    #         print(cnt, len(communities[key]))
    #         cnt += 1

    with open("data/history/user_history_date=119.pickle", 'rb') as f:
        record = pickle.load(f)

    with open("data/history/record_paperid2uid_data=119.pickle", 'rb') as f:
        record_paperid2uid = pickle.load(f)

    with open("data/author_info.pickle", 'rb') as f:
        author_info = pickle.load(f)

    with open("data/Paper_title.pickle", 'rb') as f:
        Paper_title = pickle.load(f)

    with open("data/paperid2com.json", 'r') as f:
        paperid2com = json.load(f)

    pid = 348096325
    print(Paper_title[pid])
    commid = paperid2com[str(pid)]

    with open("node2vec/embeddings/"+str(commid)+".csv.pkl", 'rb') as f:
        embeddings = pickle.load(f)
    with open("node2vec/data/"+str(commid)+"_id2tmpid.json", 'r') as f:
        id2tmpid = json.load(f)
    with open("node2vec/data/"+str(commid)+"_tmpid2id.json", 'r') as f:
        tmpid2id = json.load(f)
    with open("data/paperid2id.json", 'r') as f:
        paperid2id = json.load(f)
    with open("data/id2paperid.json", 'r') as f:
        id2paperid = json.load(f)

    print(embeddings.shape)

    embeddings /= np.sqrt(np.sum(embeddings**2, axis=1)).reshape(-1, 1)

    similarity = embeddings.dot(embeddings[id2tmpid[str(paperid2id[str(pid)])]])
    ranking = sorted(enumerate(similarity), key=lambda x: x[1], reverse=True)
    for paper in ranking[:20]:
        print(Paper_title[id2paperid[str(tmpid2id[str(paper[0])])]], paper[1], id2paperid[str(tmpid2id[str(paper[0])])])

    # for uid in record:
    #     print(uid, len(record[uid]), record[uid][:10])

    # for pid in record_paperid2uid:
    #     print(record_paperid2uid[pid])
    #     exit()
