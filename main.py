import streamlit as st
from fileHandler import csvHandler,jsonHandler
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt


st.title('Tubes Prokom')
st.header('Produksi Minyak Mentah')
ch_ = csvHandler('produksi_minyak_mentah.csv')
jh_ = jsonHandler('kode_negara_lengkap.json')

#--Poin (a)--
df_ = ch_.dataFrame
df_info = jh_.dataFrame
negara_li = df_info['name'].tolist()

negara = st.selectbox('Pilih negara : ',negara_li) 


kode = df_info[df_info['name']==negara]['alpha-3'].tolist()[0]


st.write('Kode negara : ',kode)
st.write('Negara : ',negara)

x_ = df_[df_['kode_negara']==kode]['tahun'].tolist()
y_ = df_[df_['kode_negara']==kode]['produksi'].tolist()

reg = LinearRegression()
reg.fit(np.array(x_).reshape(-1,1),np.array(y_))
m = reg.coef_[0]
c = reg.intercept_
y_trend = [m*x+c for x in x_]
if c >= 0:
    equation = 'y={m:.2f}x+{c:.2f}'.format(m=m,c=c)
else:
    equation = 'y={m:.2f}x{c:.2f}'.format(m=m,c=c)

dic = {'tahun':x_,'produksi':y_}
st.write(pd.DataFrame(dic))

plotting = st.selectbox('Pilih tipe plotting : ',['tipe 1','tipe 2'])

if plotting == 'tipe 1':
    plt.title('Data Produksi {}'.format(negara))
    plt.plot(x_,y_,label='Actual')
    plt.plot(x_,y_trend,label='Trendline\n{}'.format(equation))
    plt.xlabel('Tahun')
    plt.ylabel('Produksi')
    plt.legend()
    st.pyplot(plt)
else:
    dic['trendline'] = y_trend
    fig = px.scatter(pd.DataFrame(dic),x='tahun',y='produksi',trendline='lowess',trendline_options=dict(frac=0.1))
    st.plotly_chart(fig)

#--Poin (b)--
st.write()
st.write()
st.header('Bagian B COKK')


B = st.sidebar.number_input("Berapa besar negara?", min_value=1, max_value=None)
T = st.sidebar.number_input("Tahun produksi", min_value=1971, max_value=2015)

df = df_
dfJ = df_info

df = df[df['tahun']==T]
kode_negara = df[df['tahun']==T]['kode_negara'].tolist()
# produksi = df[df['tahun']==T]['produksi'].tolist()

produksi_maks = []
negara_pertahun = []

kode_negara = list(dict.fromkeys(kode_negara))
for kode in kode_negara:
    try:
        produksi = df[df['kode_negara']==kode]['produksi'].tolist()
        negara = dfJ[dfJ['alpha-3']==kode]['name'].tolist()[0]
        produksi_maks.append(max(produksi))
        negara_pertahun.append(negara)
    except:
        continue
        
dic = {'negara':negara_pertahun,'produksi_maks':produksi_maks}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values('produksi_maks',ascending=False).reset_index()

plt.clf() # clear the figure

#tulisan nanti lu aja ya, gua update ke github dulu

plt.title('{B} Negara dengan Produksi Terbesar pada Tahun {T}'.format(B=B,T=T))
plt.bar(df__['negara'][:B],df__['produksi_maks'][:B],width=0.9, bottom=None, align="center",
            color="lightblue", edgecolor="aquamarine", data=None, zorder=3)
plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
plt.xlabel('negara')
plt.ylabel('produksi_maksimum')

st.write('Input banyak negara dan tahun di kiri')
st.pyplot(plt)

#--Poin (c)--
st.write()
st.write()
st.header('Bagian C COKK')


B_ = st.sidebar.number_input("Berapa besar negara (Bagian C)?", min_value=1, max_value=None)

df = df_
dfJ = df_info

kode_negara = df['kode_negara'].tolist()
kode_negara = list(dict.fromkeys(kode_negara))

produksi_total = []
negara_ = []

for kode in kode_negara:
    try:
        produksi = df[df['kode_negara']==kode]['produksi'].tolist()
        negara = dfJ[dfJ['alpha-3']==kode]['name'].tolist()[0]
        produksi_total.append(np.sum(np.array(produksi)))
        negara_.append(negara)
    except:
        continue
        
dic = {'negara':negara_,'produksi_total':produksi_total}
df__ = pd.DataFrame(dic)
df__ = df__.sort_values('produksi_total',ascending=False).reset_index()

plt.clf() # clear the figure

#tulisan nanti lu aja ya, gua update ke github dulu

plt.title('{B} Negara dengan Produksi Terbesar Kumulatif'.format(B=B_))
plt.bar(df__['negara'][:B_],df__['produksi_total'][:B_],width=0.9, bottom=None, align="center",
            color="lightblue", edgecolor="aquamarine", data=None, zorder=3)
plt.grid(True, color="grey", linewidth="0.7", linestyle="-.", zorder=0)
plt.xlabel('negara')
plt.ylabel('produksi_total')

st.write('Input banyak negara')
st.pyplot(plt)

#--Poin (d)--
st.write()
st.write()
st.header('Bagian D COKK')

T_ = st.sidebar.number_input("Summary Tahun Produksi", min_value=1971, max_value=2015)

df = ch_.dataFrame
dfJ = jh_.dataFrame

tahun = list(dict.fromkeys(df['tahun'].tolist()))

dic_maks = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_min = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}
dic_zero = {'negara':[],
            'kode_negara':[],
            'region':[],
            'sub_region':[],
            'produksi':[],
            'tahun':tahun}

for t in tahun:
    df_per_tahun = df[df['tahun']==t]
    produksi = np.array(df_per_tahun['produksi'].tolist())
    maks_prod = max(produksi)
    min_prod = min([p for p in produksi if p != 0])
    zero_prod = min([p for p in produksi if p == 0])
    # maksimum
    kode_negara = df_per_tahun[df_per_tahun['produksi']==maks_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_maks['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_maks['kode_negara'].append(kode_negara)
    dic_maks['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_maks['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_maks['produksi'].append(maks_prod)
    # minimum != 0
    kode_negara = df_per_tahun[df_per_tahun['produksi']==min_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_min['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_min['kode_negara'].append(kode_negara)
    dic_min['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_min['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_min['produksi'].append(min_prod)
    # zero == 0
    kode_negara = df_per_tahun[df_per_tahun['produksi']==zero_prod]['kode_negara'].tolist()[0]
    if kode_negara == 'WLD':
        kode_negara = 'WLF'
    dic_zero['negara'].append(dfJ[dfJ['alpha-3']==kode_negara]['name'].tolist()[0])
    dic_zero['kode_negara'].append(kode_negara)
    dic_zero['region'].append(dfJ[dfJ['alpha-3']==kode_negara]['region'].tolist()[0])
    dic_zero['sub_region'].append(dfJ[dfJ['alpha-3']==kode_negara]['sub-region'].tolist()[0])
    dic_zero['produksi'].append(zero_prod)

df_maks = pd.DataFrame(dic_maks)
df_min = pd.DataFrame(dic_min)
df_zero = pd.DataFrame(dic_zero)

st.write('Info Produksi Maksimum Tahun ke-{}'.format(T_))
st.write(df_maks[df_maks['tahun']==T_])

st.write('Tabel Maks per Tahun')
st.write(df_maks)

st.write('Info Produksi Minimum (Not Zero) Tahun ke-{}'.format(T_))
st.write(df_min[df_min['tahun']==T_])

st.write('Tabel Min (Not Zero) per Tahun')
st.write(df_min)

st.write('Info Produksi Zero Tahun ke-{}'.format(T_))
st.write(df_zero[df_zero['tahun']==T_])

st.write('Tabel Zero per Tahun')
st.write(df_zero)