import json
import numpy as np
import pandas as pd
from tqdm import tqdm

def record(paperid):
    global paperid2id, id2paperid, currentid
    if paperid not in paperid2id:
        paperid2id[paperid] = currentid
        id2paperid[currentid] = paperid
        currentid += 1

if __name__ == "__main__":
    edges = np.load("../data/edges.npy")
    with open("../data/communities.json", 'r') as f:
        communities = json.load(f)

    cnt = 0
    for comm_id in communities:
        tmp = set(communities[comm_id])
        if len(communities[comm_id]) < 20:
            continue
        edge_subset = []
        for edge in tqdm(edges):
            if edge[0] in tmp and edge[1] in tmp:
                edge_subset.append([edge[0], edge[1]])
        edge_subset = np.array(edge_subset)
        paperid2id = dict()
        id2paperid = dict()
        currentid = 0
        for edge in edge_subset:
            u = int(edge[0])
            v = int(edge[1])
            record(u)
            record(v)
            edge[0] = paperid2id[u]
            edge[1] = paperid2id[v]

        result = pd.DataFrame({'source': edge_subset[:, 0],
                               'target': edge_subset[:, 1]})
        result.to_csv("data/"+comm_id+".csv", index=False, sep=',')

        with open("data/"+comm_id+".json", 'w') as f:
            json.dump(id2paperid, f)

        cnt += 1
        print(cnt)
        print(len(communities[comm_id]))
        print(len(edge_subset))
        print("-----------------------")
