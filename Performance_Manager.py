import pandas as pd 
import datetime
import scipy
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Battery Performance Manager POC Experiment</h1>", unsafe_allow_html=True)

df = pd.read_csv('data/DemoBatteryData.csv', index_col = 0, parse_dates = ['datetime'])

battery = st.selectbox(
    'Battery:',
    ['B0005', 'B0006', 'B0007', 'B0018', 'B0025']
    )
source = df[(df.battery == battery)]


fig = px.line(source[['datetime', 'voltage_measured']].resample('1h', on = 'datetime').mean().dropna().reset_index(), x = 'datetime', y = 'voltage_measured', title='Measured Voltage Across Battery Lifetime')
st.plotly_chart(fig, use_container_width=True)


cycles = st.multiselect(
    'Cycle:',
    source.cycle.unique(),
    default = max(source.cycle.unique())
    )

col1, col2 = st.columns(2)

with col1:
    fig2 = px.line(source[source.cycle.isin(cycles)], x = 'time', y = 'voltage_load', title='Voltage Load Across Cycle Time', color = 'cycle')
    st.plotly_chart(fig2, use_container_width=True)
    fig3 = px.line(source[source.cycle.isin(cycles)], x = 'time', y = 'voltage_measured', title='Measured Voltage Across Cycle Time', color = 'cycle')
    st.plotly_chart(fig3, use_container_width=True)


with col2:
    fig4 = px.line(source[source.cycle.isin(cycles)], x = 'time', y = 'temperature_measured', title='Battery Temperature Across Cycle Time', color = 'cycle')
    st.plotly_chart(fig4, use_container_width=True)
    fig5 = px.line(source[source.cycle.isin(cycles)], x = 'time', y = 'current_measured', title='Measured Current Across Cycle Time', color = 'cycle')
    st.plotly_chart(fig5, use_container_width=True)



