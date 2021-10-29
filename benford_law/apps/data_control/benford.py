import pandas as pd
#from django.conf import settings
#from sqlalchemy import create_engine

from benford_law.views import index
from .models import DataSets
from .models import BenfordDistributions

class BenfordDataset:
    def __init__(self, df, id, col):
        self.df = df
        self.id = id
        self.col = col
        self.prep = self.df.rename(columns = {self.col: 'value'}, inplace = False)
        self.d = None

    # def save_db(self):
    #     user = settings.DATABASES['default']['USER']
    #     password = settings.DATABASES['default']['PASSWORD']
    #     database_name = settings.DATABASES['default']['NAME']
    #     self.prep['dataset_id'] = self.id
    #     # prep = self.df.rename(columns = {self.col: 'value'}, inplace = False)
    #     # print(prep)

    #     database_url = f"postgresql+psycopg2://{user}:{password}@postgres:5432/{database_name}"
    #     #print(database_url)
    #     engine = create_engine(database_url, echo = False)
    #     try:
    #         self.prep.to_sql(DataValues._meta.db_table, con=engine, if_exists='append', index=False)
    #         return "Success"
    #     except Exception as e:
    #         return 'Error while saving to database: ' + str(e)

    def get_benford_distribution(self):
        self.prep['first_number'] = self.prep['value'].astype(str).str[0] 
        self.prep['num_filter'] = self.prep['first_number'].astype(str).str.match("^[1-9]")
        self.prep.drop(self.prep[self.prep['num_filter'] != True].index, inplace = True)
        percents = self.prep['first_number'].value_counts(normalize=True)
        perc_sorted = percents.sort_index()
        print('-------------------------------------------------------------------')
        print(perc_sorted)
        print('-------------------------------------------------------------------')
        fr = perc_sorted.to_frame()
        benResults = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
        try:
            fr.insert(1, "Benford", benResults, True)
        except:
            return 'Data dont contain all leading numbers in range of 1 to 9.'
        d = fr.to_dict()
        self.d = d
        return d

    def save_results(self):
        res_list = []
        dv = DataSets.objects.get(id = self.id)
        print(dv)
        for i in range(1,10):
            res_list.append(BenfordDistributions(dataset= dv, 
                                                number=i, 
                                                occurence=self.d['first_number'][str(i)],
                                                bensfords=self.d['Benford'][str(i)]))
        
        print(res_list)
        try:
            BenfordDistributions.objects.bulk_create(res_list)
            return 'Success'
        except Exception as e:
            return f'Error: {e}'    

        
