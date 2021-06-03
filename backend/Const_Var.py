import json
import os
import pickle
import datetime
from apis.utils import Remote_to_Local
from tqdm import tqdm
from apis.models import Record

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


HIS_TIME_OUT = 120 * 60
AUTHOR_LOCAL = {}

Author_Subset_List = list(Author_Subset)
for x in tqdm(range(0, len(Author_Subset_List), 5000)):
    subx = Author_Subset_List[x: x + 5000]
    AUTHOR_LOCAL.update(Remote_to_Local(subx))


class History_Info:
    def __init__(self):
        self.update_time = datetime.datetime.now()
        self.Fetch_Info()

    def Fetch_Info(self):

        TimeGap = datetime.timedelta(days=60)
        Last_Date = datetime.datetime.now() - TimeGap
        Rec_Month = Record.objects.filter(
            updated_time__gte=Last_Date,
            rtype=2
        )
        His = {}
        for lin in tqdm(Rec_Month):
            if lin.remote_id not in His:
                His[lin.remote_id] = []
            His[lin.remote_id].append({
                'paperid': lin.paper_id,
                'time': lin.updated_time
            })

        self.User_History, self.Rev_History = {}, {}
        for k, v in tqdm(His.items()):
            Temp = [(x['paperid'], x['time'].date()) for x in v]
            self.User_History[k] = Temp
            for rec in v:
                if rec['paperid'] not in self.Rev_History:
                    self.Rev_History[rec['paperid']] = []
                self.Rev_History[rec['paperid']].append(
                    (k, rec['time'].date())
                )

    def Update_Info(self):
        Time_Delt = datetime.datetime.now() - self.update_time
        if Time_Delt.days > 0 or Time_Delt.seconds > HIS_TIME_OUT:
            self.Fetch_Info()
            self.update_time = datetime.datetime.now()



History_Graph = History_Info()
