import time
import json
import random
import numpy as np
import pandas as pd
from tqdm import tqdm

def init_adjList_and_Ki(edges):
    N = edges.max() + 1
    adjList = []
    K_i = [0] * N
    for i in range(N):
        adjList.append(dict())
    for i in tqdm(range(edges.shape[0])):
        source = edges[i][0]
        dest = edges[i][1]
        K_i[source] += 1
        K_i[dest] += 1
        if dest in adjList[source]:
            adjList[source][dest] += 1
        else:
            adjList[source][dest] = 1
        if source in adjList[dest]:
            adjList[dest][source] += 1
        else:
            adjList[dest][source] = 1
    return adjList, K_i

def record(paperid):
    global paperid2id, id2paperid, currentid
    if paperid not in paperid2id:
        paperid2id[paperid] = currentid
        id2paperid[currentid] = paperid
        currentid += 1

if __name__ == "__main__":

    EDGE_PATH = "data/edges_real.csv"

    edges = pd.read_csv(EDGE_PATH).values

    paperid2id = dict()
    id2paperid = dict()
    currentid = 0
    for edge in tqdm(edges):
        u = int(edge[0])
        v = int(edge[1])
        record(u)
        record(v)
        edge[0] = paperid2id[u]
        edge[1] = paperid2id[v]

    with open("data/id2paperid.json", "w") as f:
        json.dump(id2paperid, f)

    np.save("data/edges.npy", edges)

    # edges = np.load("data/edges.npy")
    # with open("data/id2paperid.json", "r") as f:
    #     id2paperid = json.load(f)
    # print(edges[:10])
