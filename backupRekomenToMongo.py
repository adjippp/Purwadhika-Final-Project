import sys
import pandas as pd
import pymongo
import json

mng_client = pymongo.MongoClient('localhost', 27017)
mng_db = mng_client['rekomendasi']
collection_name = 'top10'
collection_name2 = 'rekomen'

dbtop10 = mng_db[collection_name]
dbrekomen = mng_db[collection_name2]

dataTop = pd.read_csv('popularityRecommendation.csv')
dataRekom = pd.read_csv('similarityRecommendation.csv')

dataTop_json = json.loads(dataTop.to_json(orient='records'))
dataRekom_json = json.loads(dataRekom.to_json(orient='records'))

dbtop10.insert(dataTop_json)
dbrekomen.insert(dataRekom_json)