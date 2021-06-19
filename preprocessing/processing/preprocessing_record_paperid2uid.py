import pickle
from tqdm import tqdm

if __name__ == "__main__":

    with open("data/user_history.pickle", 'rb') as f:
        user_history = pickle.load(f)

    record_paperid2uid = dict()
    for uid in tqdm(user_history):
        for song in user_history[uid]:
            if song[0] not in record_paperid2uid:
                record_paperid2uid[song[0]] = [(uid, song[1])]
            else:
                record_paperid2uid[song[0]].append((uid, song[1]))

    for songid in tqdm(record_paperid2uid):
        record_paperid2uid[songid] = sorted(record_paperid2uid[songid], key=lambda x: x[1])

    with open("data/record_paperid2uid.pickle", 'wb') as f:
        pickle.dump(record_paperid2uid, f)
