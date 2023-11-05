import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import streamlit as st
sns.set(style='dark')

# Fungsi menghitung AQI
def calculate_aqi(C_p, breakpoints):
    I_low, I_high, C_low, C_high = breakpoints['I_low'], breakpoints['I_high'], breakpoints['C_low'], breakpoints['C_high']
    
    if C_p > C_high:
        return I_high
    
    return ((I_high - I_low) / (C_high - C_low)) * (C_p - C_low) + I_low

# 7 Variable breakpoints
pm25_breakpoints_1 = {'I_low': 0, 'I_high': 50, 'C_low': 0, 'C_high': 12}
pm25_breakpoints_2 = {'I_low': 51, 'I_high': 100, 'C_low': 12.1, 'C_high': 35.4}
pm25_breakpoints_3 = {'I_low': 101, 'I_high': 150, 'C_low': 35.5, 'C_high': 55.4}
pm25_breakpoints_4 = {'I_low': 151, 'I_high': 200, 'C_low': 55.5, 'C_high': 150.4}
pm25_breakpoints_5 = {'I_low': 201, 'I_high': 300, 'C_low': 150.5, 'C_high': 250.4}
pm25_breakpoints_6 = {'I_low': 301, 'I_high': 400, 'C_low': 250.5, 'C_high': 350.4}
pm25_breakpoints_7 = {'I_low': 401, 'I_high': 500, 'C_low': 350.5, 'C_high': 500}

# Fungsi menentukan breakpoints berdasarkan konsentrasi PM2.5
def choose_breakpoints(C_p):
    if C_p <= pm25_breakpoints_1['C_high']:
        return pm25_breakpoints_1
    elif C_p <= pm25_breakpoints_2['C_high']:
        return pm25_breakpoints_2
    elif C_p <= pm25_breakpoints_3['C_high']:
        return pm25_breakpoints_3
    elif C_p <= pm25_breakpoints_4['C_high']:
        return pm25_breakpoints_4
    elif C_p <= pm25_breakpoints_5['C_high']:
        return pm25_breakpoints_5
    elif C_p <= pm25_breakpoints_6['C_high']:
        return pm25_breakpoints_6
    else:
        return pm25_breakpoints_7

# Visualisasi perbandingan AQI dari 3 stations
def plot_aqi_comparison(df, interval_column, station_column, aqi_column):
    plt.figure(figsize=(12, 8))
    for station in df[station_column].unique():
        station_data = df[df[station_column] == station]
        plt.plot(station_data[interval_column], station_data[aqi_column], label=station, marker='o')

    plt.xlabel('Date')
    plt.ylabel('AQI')
    plt.legend()

    plt.gcf().autofmt_xdate()

    st.pyplot(plt)

# Fungsi untuk memplot nilai AQI min dan maks dari setiap stasiun
def plot_min_max_aqi(df, interval_column, station_column, aqi_column):
    min_aqi = df.groupby(station_column)[aqi_column].min()
    max_aqi = df.groupby(station_column)[aqi_column].max()

    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    ax[0].bar(min_aqi.index, min_aqi.values, color='blue')
    ax[0].set_title('Minimum AQI from Each Station', fontsize=18)
    ax[0].set_xlabel('Station')
    ax[0].set_ylabel('AQI')

    ax[1].bar(max_aqi.index, max_aqi.values, color='red')
    ax[1].set_title('Maximum AQI from Each Station', fontsize=18)
    ax[1].set_xlabel('Station')
    ax[1].set_ylabel('AQI')

    st.pyplot(fig)

# Fungsi untuk memplot konsentrasi NO2 dari station Dongsi dan Huairou
def plot_no2_dongsi_huairou(df, interval_column, station_column, no2_column):
    plt.figure(figsize=(12, 8))
    for station in df[station_column].unique():
        station_data = df[df[station_column] == station]
        color = 'orange' if station == 'Dongsi' else 'green'
        plt.plot(station_data[interval_column], station_data[no2_column], label=station, marker='o', color=color)

    plt.xlabel('Date')
    plt.ylabel('NO2')
    plt.legend()

    plt.gcf().autofmt_xdate()

    st.pyplot(plt)

# Fungsi untuk memplot konsentrasi CO dan kadar RAIN di Dongsi
def plot_co_rain_dongsi(df, co_column, rain_column):
    fig, ax1 = plt.subplots(figsize=(12, 8))

    # Plot CO concentrations
    ax1.plot(df['date'], df[co_column], label='CO', color='orange')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('CO')
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left')

    # Create a secondary y-axis for rainfall
    ax2 = ax1.twinx()
    ax2.plot(df['date'], df[rain_column], label='Rain', linestyle='--', color='#39A7FF')
    ax2.set_ylabel('RAIN')
    ax2.tick_params(axis='y')
    ax2.legend(loc='upper right')


    plt.gcf().autofmt_xdate()
    st.pyplot(fig)

# Load cleaned data
all_df = pd.read_csv('all_data.csv')
all_df['date'] = pd.to_datetime(all_df['date'])

# Filter data
min_date = all_df["date"].min()
max_date = all_df["date"].max()

with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>Air Quality Analysis</h1> <br>", unsafe_allow_html=True)
    
    # Membuat select box untuk menentukan interval waktu
    interval_analysis = st.selectbox(
        label="Analysis Time Interval",
        options=('Yearly', 'Monthly', 'Daily')
    )

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Time Span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["date"] >= str(start_date)) & 
                (all_df["date"] <= str(end_date))]

st.header('Air Quality Analysis Dashboard :dash:')

st.subheader('Average AQI Based on PM2.5 at Changping, Dongsi, and Huairou Stations')

# Perform AQI analysis based on the selected interval
if interval_analysis == 'Yearly':
    yearly_df = main_df.groupby([main_df['date'].dt.year, 'station'])['PM2.5'].mean().reset_index()
    yearly_df['date'] = yearly_df['date'].astype(str)
    yearly_df['AQI'] = yearly_df['PM2.5'].apply(lambda x: calculate_aqi(x, choose_breakpoints(x))).round()
    plot_aqi_comparison(yearly_df, 'date', 'station', 'AQI')     
    plot_min_max_aqi(yearly_df, 'date', 'station', 'AQI')
elif interval_analysis == 'Monthly':
    monthly_df = main_df.groupby([main_df['date'].dt.to_period("M"), 'station'])['PM2.5'].mean().reset_index()
    monthly_df['date'] = monthly_df['date'].astype(str)
    monthly_df['AQI'] = monthly_df['PM2.5'].apply(lambda x: calculate_aqi(x, choose_breakpoints(x))).round()
    plot_aqi_comparison(monthly_df, 'date', 'station', 'AQI')
    plot_min_max_aqi(monthly_df, 'date', 'station', 'AQI')
elif interval_analysis == 'Daily':
    daily_df = main_df.copy() # Copy dataframe dilakukan biar namanya gampang diidentifikasi dan konsisten
    daily_df['AQI'] = daily_df['PM2.5'].apply(lambda x: calculate_aqi(x, choose_breakpoints(x))).round()
    daily_df['date'] = daily_df['date'].dt.date  
    plot_aqi_comparison(daily_df, 'date', 'station', 'AQI')
    plot_min_max_aqi(daily_df, 'date', 'station', 'AQI')

st.subheader('NO2 Concentrations Between Urban (Dongsi) and Rural (Hairou) Stations')

dongsi_huairou_df = main_df[(main_df['station'] == 'Dongsi') | (main_df['station'] == 'Huairou')]
# Perform NO2 Comparison on rural and urban area
if interval_analysis == 'Yearly':
    yearly_no2_df = dongsi_huairou_df.groupby([dongsi_huairou_df['date'].dt.year, 'station'])['NO2'].mean().reset_index()
    yearly_no2_df['date'] = yearly_no2_df['date'].astype(str)
    plot_no2_dongsi_huairou(yearly_no2_df, 'date', 'station', 'NO2')
elif interval_analysis == 'Monthly':
    monthly_no2_df = dongsi_huairou_df.groupby([dongsi_huairou_df['date'].dt.to_period("M"), 'station'])['NO2'].mean().reset_index()
    monthly_no2_df['date'] = monthly_no2_df['date'].astype(str)
    plot_no2_dongsi_huairou(monthly_no2_df, 'date', 'station', 'NO2')
elif interval_analysis == 'Daily':
    daily_no2_df = dongsi_huairou_df.copy()
    daily_no2_df['date'] = daily_no2_df['date'].dt.date  # Display only the date part
    plot_no2_dongsi_huairou(daily_no2_df, 'date', 'station', 'NO2')

st.subheader('Carbon Monoxide (CO) concentrations during rainy periods in Dongsi')

dongsi_df = main_df[main_df['station'] == 'Dongsi']

col1, col2 = st.columns(2)

with col1:
    dry_days = len(dongsi_df[dongsi_df['RAIN'] == 0])
    st.metric("Dry Days", value=dry_days)

with col2:
    rainy_days = len(dongsi_df[dongsi_df['RAIN'] > 0])
    st.metric("Rainy Days", value=rainy_days)

if interval_analysis == 'Yearly':
    yearly_co_rain_df = dongsi_df.groupby([dongsi_df['date'].dt.year, 'station'])[['CO', 'RAIN']].mean().reset_index()
    yearly_co_rain_df['date'] = yearly_co_rain_df['date'].astype(str)
    plot_co_rain_dongsi(yearly_co_rain_df, 'CO', 'RAIN')
elif interval_analysis == 'Monthly':
    monthly_co_rain_df = dongsi_df.groupby([dongsi_df['date'].dt.to_period("M"), 'station'])[['CO', 'RAIN']].mean().reset_index()
    monthly_co_rain_df['date'] = monthly_co_rain_df['date'].astype(str)
    plot_co_rain_dongsi(monthly_co_rain_df, 'CO', 'RAIN')
elif interval_analysis == 'Daily':
    daily_co_rain_df = dongsi_df.copy()
    daily_co_rain_df['date'] = daily_co_rain_df['date'].dt.date
    plot_co_rain_dongsi(daily_co_rain_df, 'CO', 'RAIN')

