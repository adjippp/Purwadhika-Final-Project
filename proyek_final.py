'''
python-3.6 -m pip install

cd $HOME
cd venv
source bin/activate
'''

'''
pada modul kali ini, saya mencoba membuat program rekomendasi produk 
pada customer berdasarkan data pembelian customer tersebut
yang akan di lakukan adalah transform dan normalisasi data
mengevaluasi performa model machine learning
memilih model yang optimal (Popularity, Cosine, dan Pearson)
input : customer ID
output: ranked product ID
'''
#install dahulu sebelum menggunakan turicreate sudo apt-get install libatlas-base-dev
#jalankan file python dengan python3 proyek.py
import pandas as pd
import numpy as np
import time
import turicreate as tc

'''
tujuan awal untuk persiapan data adalah dengan melakukan break down masing-masing list 
dari item dalam kolom products menjadi baris dan menghitung jumlah produk yang di beli oleh user
'''
customers = pd.read_csv('biodata_customer.csv')
transactions = pd.read_csv('datatransaksi.csv')
transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])
# print(customers.head())
# print(transactions.head())

'''
membuat data user, barang, dan target
user memiliki customerId, productId, and purchase_count
'''
data = pd.melt(transactions.set_index('customerId')['products'].apply(pd.Series).reset_index(), 
             id_vars=['customerId'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['customerId', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})

data['productId'] = data['productId'].astype(int)
# print(data.head()) # menampilkan customerID dengan produk yang dibeli dan jumlah pembelian

'''
membuat dummy untuk menandai apakah customer membeli barang tersebut atau tidak
ditandai dengan angka 1 jika customer membeli barang tersebut
'''
def create_data_dummy(data):
    data_dummy = data.copy()
    data_dummy['purchase_dummy'] = 1
    return data_dummy

data_dummy = create_data_dummy(data)
# print(data_dummy.head())


'''
normalisasi/penskalaan value (purchase count) produk dari semua user (frekuensi pembelian)
'''
df_matrix = pd.pivot_table(data, values='purchase_count', index='customerId', columns='productId')
# print(df_matrix.head()) #menampilkan dataframe, customerId menjadi indeks baris, productID menjadi kolom, value dari kolom tersebut adalah banyaknya pembelian
df_matrix_norm = (df_matrix-df_matrix.min())/(df_matrix.max()-df_matrix.min())
# print(df_matrix_norm.head()) # hasil dataframe setelah di normalisasi
d = df_matrix_norm.reset_index() 
d.index.names = ['scaled_purchase_freq'] 
data_norm = pd.melt(d, id_vars=['customerId'], value_name='scaled_purchase_freq').dropna()
# print(data_norm.shape) #hasil 133585, 3
# print(data_norm.head()) #menampilkan data yang sudah di normalisasi/di skala kan


# hal-hal di atas dapat dilakukan dengan function dibawah
# def normalize_data(data):
#     df_matrix = pd.pivot_table(data, values='purchase_count', index='customerId', columns='productId')
#     df_matrix_norm = (df_matrix-df_matrix.min())/(df_matrix.max()-df_matrix.min())
#     d = df_matrix_norm.reset_index()
#     d.index.names = ['scaled_purchase_freq']
#     return pd.melt(d, id_vars=['customerId'], value_name='scaled_purchase_freq').dropna()

'''
setelah melakukan hal di atas, kita lakukan train split test
'''
def split_data(data):
    '''
    Splits dataset menjadi training and test set.
    
    Args:
        data (pandas.DataFrame)
        
    Returns
        train_data (tc.SFrame)
        test_data (tc.SFrame)
    '''
    sf=tc.SFrame(data)
    train, test = sf.random_split(.8)
    train_data = tc.SFrame(train)
    test_data = tc.SFrame(test)
    return train_data, test_data

'''
Kita sudah mendapatkan 3 dataframe, yaitu:
dataframe murni hasil olah data di awal
dataframe dummy
lalu dataframe yang telah di normalisasi

maka kita lakukan splitting data untuk masing-masing dataframe tersebut
'''
train_data, test_data = split_data(data)
train_data_dummy, test_data_dummy = split_data(data_dummy)
train_data_norm, test_data_norm = split_data(data_norm)

'''
kita siapkan variabel penampung untuk digunakan dengan model yang di pilih
'''
user_id = 'customerId'
item_id = 'productId'
users_to_recommend = list(customers[user_id])
n_rec = 10 # jumlah item yang direkomendasikan kepada user
n_display = 30 # menampilkan isi data sebanyak n_display baris dalam dataset

def model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display):
    if name == 'popularity':
        model = tc.popularity_recommender.create(
            train_data, 
            user_id=user_id, 
            item_id=item_id, 
            target=target
            )
    elif name == 'cosine':
        model = tc.item_similarity_recommender.create(
            train_data, 
            user_id=user_id, 
            item_id=item_id, 
            target=target, 
            similarity_type='cosine'
            )
    elif name == 'pearson':
        model = tc.item_similarity_recommender.create(
            train_data, 
            user_id=user_id, 
            item_id=item_id, 
            target=target, 
            similarity_type='pearson'
            )  
    recom = model.recommend(users=users_to_recommend, k=n_rec)
    # recom.print_rows(n_display)
    return model

'''
cek hasil rekomendasi berdasarkan popularitas dari banyaknya pembelian barang
'''
name = 'popularity'
target = 'purchase_count'
pop = model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

name = 'popularity'
target = 'purchase_dummy'
pop_dummy = model(train_data_dummy, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

name = 'popularity'
target = 'scaled_purchase_freq'
pop_norm = model(train_data_norm, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

'''
cek hasil rekomendasi berdasarkan implementasi cosine similarity dari banyaknya pembelian barang
'''
name = 'cosine'
target = 'purchase_count'
cos = model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

name = 'cosine'
target = 'purchase_dummy'
cos_dummy = model(train_data_dummy, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

name = 'cosine' 
target = 'scaled_purchase_freq' 
cos_norm = model(train_data_norm, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

'''
cek hasil rekomendasi berdasarkan implementasi pearson similarity dari banyaknya pembelian barang
'''
name = 'pearson'
target = 'purchase_count'
pear = model(train_data, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

name = 'pearson'
target = 'purchase_dummy'
pear_dummy = model(train_data_dummy, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

name = 'pearson'
target = 'scaled_purchase_freq'
pear_norm = model(train_data_norm, name, user_id, item_id, target, users_to_recommend, n_rec, n_display)

'''
untuk mengevaluasi model yang akan kita pakai adalah dengan menggunakan konsep RMSE dan precision-recall, 
model yang akan digunakan untuk similarity adalah antara cosine atau pearson
precision dan recall yang baik adalah yang mendekati angka 1
'''

models_w_counts = [pop, cos, pear]
models_w_dummy = [pop_dummy, cos_dummy, pear_dummy]
models_w_norm = [pop_norm, cos_norm, pear_norm]
names_w_counts = ['Popularity Model pada Purchase Counts', 'Cosine Similarity pada Purchase Counts', 'Pearson Similarity pada Purchase Counts']
names_w_dummy = ['Popularity Model pada Purchase Dummy', 'Cosine Similarity pada Purchase Dummy', 'Pearson Similarity pada Purchase Dummy']
names_w_norm = ['Popularity Model pada Scaled Purchase Counts', 'Cosine Similarity pada Scaled Purchase Counts', 'Pearson Similarity pada Scaled Purchase Counts']

'''
Kita cek hasil evaluasi, didapatkan Overall RMSE untuk setiap Tabel 
'''
# eval_counts = tc.recommender.util.compare_models(test_data, models_w_counts, model_names=names_w_counts)
# eval_dummy = tc.recommender.util.compare_models(test_data_dummy, models_w_dummy, model_names=names_w_dummy)
# eval_norm = tc.recommender.util.compare_models(test_data_norm, models_w_norm, model_names=names_w_norm)

'''
Berdasarkan hasil RMSE didapatkan (diambil jumlah RMSE terkecil antara cosine dan pearson)
Popularity Model pada Purchase Counts           : 1.0445724661886604
Cosine Similarity pada Purchase Counts          : 1.8855883326742047
Pearson Similarity pada Purchase Counts         : 1.0418558299886829

Popularity Model pada Purchase Dummy            : 0.0
Cosine Similarity pada Purchase Dummy           : 0.9695553323563083
Pearson Similarity pada Purchase Dummy          : 1.0

Popularity Model pada Scaled Purchase Counts    : 0.13324126309457496
Cosine Similarity pada Scaled Purchase Counts   : 0.1595290559448553
Pearson Similarity pada Scaled Purchase Counts  : 0.13296416935613467

karena hasil skoring dari data yang di normalisasi bernilai 0 maka kita gunakan data dummy untuk merekomendasikan barang

dari nilai di atas kita mendapatkan nilai antara cosine dan pearson pada data dummy
maka dipilih cosine karena nilai RMSE yang paling kecil di antara kedua similarity tersebut
'''

final_model = tc.item_similarity_recommender.create(
    tc.SFrame(data_dummy), 
    user_id=user_id, 
    item_id=item_id, 
    target='purchase_dummy', 
    similarity_type='cosine'
    )
recom = final_model.recommend(users=users_to_recommend, k=n_rec)
df_recomm = recom.to_dataframe()
# print(df_recomm)
# df_recomm = df_recomm.drop(columns='score')


final_modelTop10 = tc.popularity_recommender.create(
    tc.SFrame(data), 
    user_id=user_id, 
    item_id=item_id, 
    target='purchase_count'
    )
top10 = final_modelTop10.recommend(users=users_to_recommend, k=n_rec)
df_top10 = top10.to_dataframe()
df_top10 = df_top10.drop(columns='score')
# print(df_top10)
df_recomm.to_csv('similarityRecommendation.csv')
df_top10.to_csv('popularityRecommendation.csv')