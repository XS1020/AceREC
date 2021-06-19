import json
import time
import pickle
import random
import numpy as np
from tqdm import tqdm
from datetime import datetime

if __name__ == "__main__":
    with open("data/paper_citation_year.pickle", 'rb') as f:
        paper_citation_year = pickle.load(f)
    with open("data/Field_paper.pickle", 'rb') as f:
        Field_paper = pickle.load(f)

    currentYear = datetime.now().year

    citation_time_rank_by_fieldid = dict()
    for fieldid in tqdm(Field_paper):
        tmp_papers = [(paperid, paper_citation_year[paperid][0]/np.sqrt(currentYear-paper_citation_year[paperid][1]+1)) for paperid in Field_paper[fieldid]]
        tmp_papers = sorted(tmp_papers, key=lambda x: x[1], reverse=True)[:100]
        tmp_papers = [paper[0] for paper in tmp_papers]
        citation_time_rank_by_fieldid[fieldid] = tmp_papers

    with open("data/citation_time_rank_by_fieldid.pickle", 'wb') as f:
        pickle.dump(citation_time_rank_by_fieldid, f)
