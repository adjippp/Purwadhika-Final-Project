import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
barang=pd.read_csv('produk_lazada.csv',delimiter=',')
idChanger = np.arange(0,len(barang),1)
barang['simple_sku'] = idChanger
barang=barang.fillna('')
barang=barang.drop(columns=['simple_sku','image_url_2','image_url_3','image_url_4','image_url_5','tracking_link'])
def searchProduk(nama):
    pd.set_option('display.max_colwidth', -1)
    barang['lower'] = barang['product_name'].str.lower()
    hasil = barang.loc[:,['product_name','sale_price','discounted_percentage','discounted_price']][barang['lower'].str.contains(nama.lower())].rename(columns={'product_name':'Nama','sale_price':'Harga','discounted_percentage':'Diskon (%)','discounted_price':'Harga Setelah Diskon'}).reset_index().drop(['index'],axis=1)
    return hasil

# print(searchProduk('acer'))
# searchProduk('acer')