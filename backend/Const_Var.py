import json
import os
import pickle
import datetime
import torch
from tqdm import tqdm

from backend.settings import BASE_DIR

print('[INFO] Loading Constances')

Mapping_Path = os.path.join(BASE_DIR, 'mapping.json')

Paper_Pdf_Mapping = {}
with open(Mapping_Path) as Fin:
    Paper_Pdf_Mapping = json.load(Fin)

Paper_Subset_dir = os.path.join(BASE_DIR, 'Paper_Subset.pkl')
with open(Paper_Subset_dir, 'rb') as Fin:
    Paper_Subset = pickle.load(Fin)

with open(os.path.join(BASE_DIR, 'Author_IDs.pickle'), 'rb') as Fin:
    Author_Subset = pickle.load(Fin)

with open(os.path.join(BASE_DIR, 'Embeddings.pickle'), 'rb') as Fin:
    Cheat_Embeddings = pickle.load(Fin)

with open(os.path.join(BASE_DIR, 'Paper_Id_Pos.pickle'), 'rb') as Fin:
    PaperId2Pos = pickle.load(Fin)


with open(os.path.join(BASE_DIR, 'Paper_Pos_Id.pickle'), 'rb') as Fin:
    PaperPos2Id = pickle.load(Fin)

with open(os.path.join(BASE_DIR, 'Field_List.pickle'), 'rb') as Fin:
    Field_list = pickle.load(Fin)

print('[INFO] Done')