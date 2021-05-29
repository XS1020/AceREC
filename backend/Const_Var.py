import json
import os
import pickle

from backend.settings import BASE_DIR

Mapping_Path = os.path.join(BASE_DIR, 'mapping.json')

Paper_Pdf_Mapping = {}
with open(Mapping_Path) as Fin:
    Paper_Pdf_Mapping = json.load(Fin)

Paper_Subset_dir = os.path.join(BASE_DIR, 'Paper_Subset.pkl')
with open(Paper_Subset_dir, 'rb') as Fin:
    Paper_Subset = pickle.load(Fin)

with open(os.path.join(BASE_DIR, 'Author_IDs.pickle'), 'rb') as Fin:
    Author_Subset = pickle.load(Fin)
