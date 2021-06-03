import json
import os
import pickle
import datetime
from apis.utils import Get_Person_Record, Remote_to_Local

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

class History_Info:
    def __init__(self):
        self.update_time = datetime.datetime.now()
        self.User_History = {}
        self.Rev_History = {}

    def Fetch_Info(self):
        Author_Local = Remote_to_Local(Author_Subset)
        