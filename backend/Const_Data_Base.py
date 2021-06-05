from apis.utils import Remote_to_Local
from apis.models import Record
from Const_Var import Author_Subset
from tqdm import tqdm
import datetime
import pickle
import os
from backend.settings import BASE_DIR

HIS_TIME_OUT = 12 * 60 * 60

Author_Subset_List = list(Author_Subset)


class History_Info:
    def __init__(self, From_File=False):
        self.update_time = datetime.datetime.now()
        self.Is_New = True
        self.User_History, self.Rev_History = {}, {}
        self.Upath = os.path.join(BASE_DIR, 'User_History.pickle')
        self.Rpath = os.path.join(BASE_DIR, 'Rev_History.pickle')
        if From_File:
            with open(self.Upath, 'rb') as Fin:
                self.User_History = pickle.load(Fin)
            with open(self.Rpath, 'rb') as Fin:
                self.Rev_History = pickle.load(Fin)
            self.Is_New = False

    def Fetch_Info(self):
        print('[{}] Updateing Record Graph'.format(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        TimeGap = datetime.timedelta(days=60)
        Last_Date = datetime.datetime.now() - TimeGap
        Rec_Month = Record.objects.filter(
            updated_time__gte=Last_Date,
            rtype=2
        ).exclude(remote_id=-1)
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
        if self.Is_New or \
                Time_Delt.days > 0 or Time_Delt.seconds > HIS_TIME_OUT:
            self.Is_New = False
            self.Fetch_Info()
            self.update_time = datetime.datetime.now()
            with open(self.Upath, 'wb') as Fout:
                pickle.dump(self.User_History, Fout)
            with open(self.Rpath, 'wb') as Fout:
                pickle.dump(self.Rev_History, Fout)

    def _print(self):
        print(self.User_History)
        print(self.Rev_History)


History_Graph = History_Info(From_File=True)
