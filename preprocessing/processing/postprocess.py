import json
from tqdm import tqdm

with open("data/communities.json", "r") as f:
    communities = json.load(f)
with open("data/id2paperid.json", "r") as f:
    id2paperid = json.load(f)

communities_final = dict()
paperid2com = dict()
cnt = 0
for com in tqdm(communities.keys()):
    communities_final[com] = [id2paperid[str(idx)] for idx in communities[com]]
    for paperid in communities_final[com]:
        paperid2com[paperid] = com

with open("data/communities_final.json", "w") as f:
    json.dump(communities_final, f)
with open("data/paperid2com.json", "w") as f:
    json.dump(paperid2com, f)
