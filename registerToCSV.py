from random import randint
import pandas as pd
import numpy as np
import csv
#user mendapatkan userID,username,password
df=pd.read_csv('biodata_customer.csv')
tampungUsername=df.loc[:,'username'].values
tampungCustomerId=df.loc[:,'customerId'].values
def register(username,password,nama):
    username=username
    customerId=max(tampungCustomerId)+1
    password=password
    nama=nama
    cekAwal=False
    if(username in tampungUsername):
        return False
    else:
        cekAwal=True
    if(cekAwal==True):
        tampung=''
        tampung=str(customerId)+','+nama+','+username+','+password+'\n'
        with open('biodata_customer.csv','a') as fileku:
            fileku.write(tampung)
        return True