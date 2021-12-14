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



