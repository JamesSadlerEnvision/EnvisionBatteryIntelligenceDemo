import pandas as pd 
import datetime
import scipy
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.title('Battery Performance Manager')

df = pd.read_csv('data/DemoBatteryData.csv', index_col = 0, parse_dates = ['datetime'])

battery = st.selectbox(
    'Battery:',
    ['B0005', 'B0006', 'B0007', 'B0018', 'B0025'])
source = df[(df.battery == battery)]

fig = px.line(source[['datetime', 'voltage_measured']].resample('1h', on = 'datetime').mean().dropna().reset_index(), x = 'datetime', y = 'voltage_measured', title='Measured Voltage Across Battery Lifetime')
st.plotly_chart(fig, use_container_width=True)