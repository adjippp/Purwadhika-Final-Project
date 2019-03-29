import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt 
import io
import base64

customers = pd.read_csv('biodata_customer.csv') 
transactions = pd.read_csv('data_transaksi2.csv')
barang=pd.read_csv('produk_lazada.csv')
transactions = transactions.drop(columns='Unnamed: 2')
idChanger = np.arange(0,len(barang),1)
barang['id_produk'] = idChanger
cek=np.zeros(5)
cek2=np.array(transactions['products'][transactions['customerId']==0].head().values)
for i in range(1,11):
        cek=np.append(cek,np.array(transactions['customerId'][transactions['customerId']==i].head(10).values),axis=0)
        cek2=np.append(cek2,np.array(transactions['products'][transactions['customerId']==i].head(10).values),axis=0)

# print(cek)
# print(cek2)

# plt.figure()
# plt.subplot(121)
# plt.scatter(cek,cek2)
# plt.title('User terhadap Produk ID (Purchased)')
# plt.xlabel('Customer ID')
# plt.ylabel('Product ID (Purchased)')
# plt.grid(True)
# plt.show()
 
def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.scatter(x_coordinates, y_coordinates)
    plt.title('User terhadap Produk ID (10 Purchased Items)')
    plt.xlabel('Customer ID')
    plt.ylabel('Product ID (Purchased)')
    plt.grid(True)
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)
