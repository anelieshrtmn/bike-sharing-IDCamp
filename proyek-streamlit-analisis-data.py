import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_tren_bike_df(df):
    # df['month'] = df['dteday'].dt.month
    # df['year'] = df['dteday'].dt.year
    tren_bike_df = df.groupby(by=['year', 'month']).agg({
        'instant': 'nunique',
        'cnt_y': 'sum'
    }).reset_index()
    return tren_bike_df

def create_bike_season_df(df):
   bike_season_df = df.groupby(by="season").agg({
    "cnt_y": "sum"
    }).reset_index()
   return bike_season_df

def create_corrtemp_df(df):
    corr_temp = df['hr'].corr(df['temp_y'])
    return corr_temp

def create_corrhum_df(df):
    corr_hum = df['hr'].corr(df['hum_y'])
    return corr_hum

allbike_df = pd.read_csv('allbike_data.csv')

min_date = allbike_df["dteday"].min()
max_date = allbike_df["dteday"].max()
min_date = pd.to_datetime(min_date)
max_date = pd.to_datetime(max_date)
with st.sidebar:
    st.image('https://www.clipartbest.com/cliparts/MTL/nEx/MTLnEx6Bc.png')
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = allbike_df[(allbike_df["dteday"] >= str(start_date)) & 
                (allbike_df["dteday"] <= str(end_date))]


tren_bike_df = create_tren_bike_df(main_df)
bike_season_df = create_bike_season_df(main_df)
corr_temp = create_corrtemp_df(main_df)
corr_hum = create_corrhum_df(main_df)

st.header('Bike Sharing Dashboard :bike:')
st.write('By: Lisa Amatul Sahibah')

st.subheader('Bike Trend')
col1, = st.columns(1)
with col1:
    total = tren_bike_df.cnt_y.sum()
    st.metric("Total", value=total)
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    tren_bike_df["year"].astype(str) + '-' + tren_bike_df["month"].astype(str), 
    tren_bike_df["cnt_y"], 
    marker='o', 
    linewidth=2,
)
ax.set_title('Peminjaman Sepeda per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

st.subheader('Bike Sharing per Season')
fig, ax = plt.subplots()
seasons = bike_season_df['season'].astype(str)
counts = bike_season_df['cnt_y']
ax.bar(seasons, counts)
ax.set_title('Peminjaman sepeda per musim')
ax.set_yscale('log')
ax.set_xlabel('Musim')
ax.set_ylabel('Total Count')
st.pyplot(fig)
st.write('1: Springer')
st.write('2: Summer') 
st.write('3: Fall') 
st.write('4: Winter')

st.subheader('Bike Correlation')
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].scatter(allbike_df['hr'], allbike_df['temp_y'], alpha=0.5)
ax[0].set_title('Hubungan antara Waktu dan Suhu')
ax[0].set_xlabel('Waktu (hr)')
ax[0].set_ylabel('Suhu')
ax[1].scatter(allbike_df['hr'], allbike_df['hum_y'], alpha=0.5)
ax[1].set_title('Hubungan antara Waktu dan Kelembaban')
ax[1].set_xlabel('Waktu (hr)')
ax[1].set_ylabel('Kelembaban')
fig.tight_layout()
st.pyplot(fig)

st.caption('Proyek Analisis Data dengan Python')