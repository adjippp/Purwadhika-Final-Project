import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt 
import io
import base64

customers = pd.read_csv('biodata_customer.csv') 
transactions = pd.read_csv('datatransaksi.csv')
transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])
# print(transactions)
barang=pd.read_csv('produk_lazada.csv')
idChanger = np.arange(0,len(barang),1)
barang['productId'] = idChanger

transactions=transactions.products.apply(pd.Series).merge(transactions, left_index = True, right_index = True).drop(["products"], axis = 1) \
    .melt(id_vars = ['customerId'], value_name = "products").drop("variable", axis = 1).dropna()
transactions['products']=transactions['products'].astype(int)
transactions=transactions.sort_values(by=['customerId']).reset_index().drop(columns='index')
cek=np.array(transactions['customerId'][transactions['customerId']==0].head(10).values)
cek2=np.array(transactions['products'][transactions['customerId']==0].head(10).values)
for i in range(1,11):
        tampung1=transactions['customerId'][transactions['customerId']==i].head(10).values
        tampung2=transactions['products'][transactions['customerId']==i].head(10).values
        cek=np.append(cek,tampung1)
        cek2=np.append(cek2,tampung2)

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
