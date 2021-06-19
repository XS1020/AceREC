import os
import json
from tqdm import tqdm

if __name__ == "__main__":
    for root, dirs, files in os.walk("data/"):
        for file in tqdm(files):
            if file.endswith(".csv"):
                continue
            with open(root+file, 'r') as f:
                tmpid2id = json.load(f)
            os.remove(root+file)
            filename = file.split(".")[0]
            with open(root+filename+"_tmpid2id.json", 'w') as f:
                json.dump(tmpid2id, f)
            with open(root+filename+"_id2tmpid.json", 'w') as f:
                id2tmpid = dict()
                for tmpid in tmpid2id:
                    id2tmpid[tmpid2id[tmpid]] = int(tmpid)
                json.dump(id2tmpid, f)
