import os
import json
from tqdm import tqdm

if __name__ == "__main__":
    with open("data/id2paperid.json", 'r') as f:
        id2paperid = json.load(f)
    with open("data/paperid2id.json", 'w') as f:
        paperid2id = dict()
        for idx in tqdm(id2paperid):
            paperid2id[id2paperid[idx]] = int(idx)
        json.dump(paperid2id, f)
        print(paperid2id)
