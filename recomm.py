import pandas as pd
import numpy as np

barang=pd.read_csv('produk_lazada.csv',delimiter=',')
idChanger = np.arange(0,len(barang),1)
barang['productId'] = idChanger
barang=barang.fillna('')
barang=barang.drop(columns=['simple_sku','image_url_2','image_url_3','image_url_4','image_url_5','tracking_link'])
popularity=pd.read_csv('popularityRecommendation.csv')
similarity=pd.read_csv('similarityRecommendation.csv')
pd.set_option('display.max_colwidth', -1)

def getPopularity():
    tampungPopularitas=popularity['productId'].head(10).values
    hasil=barang[['product_name','picture_url']][barang['productId'].isin(tampungPopularitas)].reset_index().drop(columns='index')
    hasil=hasil.set_index('product_name')
    hasil=hasil['picture_url'].to_dict()
    return hasil

def getSimilarity(customerId):
    tampungCustomer=similarity['productId'][similarity['customerId']==customerId].values
    hasil=barang[['product_name','sale_price','discounted_percentage','discounted_price']][barang['productId'].isin(tampungCustomer)].rename(columns={'product_name':'Nama','sale_price':'Harga','discounted_percentage':'Diskon (%)','discounted_price':'Harga Setelah Diskon'}).reset_index().drop(['index'],axis=1)
    return hasil

# print(getPopularity())
# getSimilarity(1553)