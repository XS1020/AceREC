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

def init_GTSet(groundTruth):
    GTSet = []
    K = groundTruth[:, 1].max() + 1
    for i in range(K):
        GTSet.append(set())
    for i in range(groundTruth.shape[0]):
        GTSet[groundTruth[i][1]].add(groundTruth[i][0])
    return GTSet

def sort_by_K(array, K_i):
    X = [(array[i], K_i[i]) for i in range(len(array))]
    X = sorted(list(X), key=lambda x: x[1])
    return [x[0] for x in X]

def ranking(community, GTSet, test=False):
    Rank = []
    for GTcommunity in GTSet:
        Rank.append(len(community & GTcommunity))
    if test:
        print(len(community), Rank)
    return np.argmax(np.array(Rank))

def K_i_C(u_adj_comms, communityid):
    if communityid in u_adj_comms:
        return u_adj_comms[communityid]
    return 0

def delta_Q(u, community_v, communityid_of_each_node, K_i, K_tot, u_adj_comms, M):
    community_u = communityid_of_each_node[u]
    E_tot_D = K_tot[community_u]
    E_tot_C = K_tot[community_v]
    k_u = K_i[u]
    KiD = K_i_C(u_adj_comms, community_u)
    KiC = K_i_C(u_adj_comms, community_v)
    return 2 * (KiC - KiD) + k_u / M * (E_tot_D - E_tot_C - k_u)

def Louvain(K_i, communityid_of_each_node, adjList, N, M, test=False):
    communities = []
    for i in range(N):
        communities.append({i})
    # Iterating
    while True:
        modified = False
        K_tot = K_i.copy()

        # Phase 1. Partitioning
        print("[INFO] Partitioning")
        ite = 0
        while True:
            if test:
                print(ite, len(set(communityid_of_each_node)))
            time_0 = time.time()
            ite += 1
            converge = True
            candidate = list(range(len(communityid_of_each_node)))
            random.shuffle(candidate)
            for u in tqdm(candidate):
                Max = 0
                argMax = None
                u_adj_comms = dict()
                neighbor_u = adjList[u]
                comm_u = communityid_of_each_node[u]
                for v in neighbor_u:
                    comm_v = communityid_of_each_node[v]
                    if comm_v in u_adj_comms:
                        u_adj_comms[comm_v] += neighbor_u[v]
                    else:
                        u_adj_comms[comm_v] = neighbor_u[v]
                for comm_v in u_adj_comms:
                    if comm_u == comm_v:
                        continue
                    dQ = delta_Q(u, comm_v, communityid_of_each_node, K_i, K_tot, u_adj_comms, M)
                    if dQ > Max:
                        Max = dQ
                        argMax = comm_v
                if argMax is not None:
                    converge = False
                    modified = True
                    K_tot[comm_u] -= K_i[u]
                    communityid_of_each_node[u] = argMax
                    K_tot[argMax] += K_i[u]
            time_1 = time.time()
            if test:
                print(time_1 - time_0)
            if converge:
                break

        # print(communityid_of_each_node)

        if not modified:
            break

        # Phase 2. Restructuring
        print("[INFO] Reconstructing")
        commSet = set(list(communityid_of_each_node))
        id_dict = dict()
        for i, c in tqdm(enumerate(commSet)):
            id_dict[c] = i
        new_communities = []
        new_adjList = []
        new_K_i = []
        for i, comm in tqdm(enumerate(commSet)):
            tmp_com = set()
            tmp_adj = dict()
            tmp_Ki = 0
            community = set(np.where(communityid_of_each_node == comm)[0])
            for c in community:
                tmp_com = tmp_com | communities[c]
                tmp_Ki += K_i[c]
                for v in adjList[c]:
                    com = id_dict[communityid_of_each_node[v]]
                    if com == i:
                        continue
                    if com in tmp_adj:
                        tmp_adj[com] += adjList[c][v]
                    else:
                        tmp_adj[com] = adjList[c][v]
            new_communities.append(tmp_com)
            new_adjList.append(tmp_adj)
            new_K_i.append(tmp_Ki)
        communities, adjList, K_i = new_communities, new_adjList, new_K_i
        communityid_of_each_node = np.array(range(len(communities)))
    return communities

if __name__ == "__main__":

    print("[INFO] Read in data")
    EDGE_PATH = "data/edges.npy"
    edges = np.load(EDGE_PATH)

    print("[INFO] Prepare some variables")
    N = edges.max() + 1             # Number of nodes
    M = edges.shape[0]              # Number of edges
    adjList, K_i = init_adjList_and_Ki(edges)
    communityid_of_each_node = np.array(range(N))

    print("[INFO] Run louvain algorithm")
    communities = Louvain(K_i, communityid_of_each_node, adjList, N, M, test=True)

    print("[INFO] Output program result")
    output = dict()
    for i, comm in enumerate(communities):
        output[i] = list(comm)
    with open("data/communities.json", "w") as f:
        json.dump(output, f)
