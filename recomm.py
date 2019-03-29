import pandas as pd
import numpy as np

barang=pd.read_csv('produk_lazada.csv',delimiter=',')
idChanger = np.arange(0,len(barang),1)
barang['productId'] = idChanger
barang=barang.fillna('')
barang=barang.drop(columns=['simple_sku','image_url_2','image_url_3','image_url_4','image_url_5','tracking_link'])
popularity=pd.read_csv('popularityRecommendation.csv')
similarity=pd.read_csv('similarityRecommendation.csv')


def getPopularity():
    tampungPopularitas=popularity['productId'].head(10).values
    hasil=barang['product_name'][barang['productId'].isin(tampungPopularitas)].reset_index().drop(columns='index')
    print(hasil)
def getSimilarity(customerId):
    tampungCustomer=similarity['productId'][similarity['customerId']==customerId].values
    hasil=barang['product_name'][barang['productId'].isin(tampungCustomer)].reset_index().drop(columns='index')
    print(hasil)

# getPopularity()
# getSimilarity(1553)