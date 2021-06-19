import pickle

if __name__ == "__main__":
    with open("data/author_info_new.pickle", 'rb') as f:
        author_info = pickle.load(f)

    author_info_dict = dict()
    for author in author_info:
        author['paper_count'] = len(author['paper_id'])
        author_info_dict[author['id']] = author

    with open("data/author_info.pickle", 'wb') as f:
        pickle.dump(author_info_dict, f)
