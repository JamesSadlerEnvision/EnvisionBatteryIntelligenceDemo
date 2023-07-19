import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Battery Performance Manager POC Experiment</h1>", unsafe_allow_html=True)

df = pd.read_csv('data/DemoBatteryData.csv', index_col = 0, parse_dates = ['datetime'])
capacity_df = pd.read_csv('data/DemoCapacityData.csv', index_col = 0, parse_dates = ['datetime'])

battery = st.selectbox(
    'Battery:',
    ['B0005', 'B0006', 'B0007', 'B0018', 'B0025']
    )
source = df[(df.battery == battery)]
sourceCapacity = capacity_df[(capacity_df.battery == battery)]


col1, col2, col3 = st.columns(3)

with col1:
    fig10 = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = source[source.battery == battery].capacity.iloc[-1],
    title = {'text': "Battery Capacity (Ahr)"},
    domain = {'x': [0, 1], 'y': [0, 1]}
    ))
    st.plotly_chart(fig10, use_container_width=True)




fig = px.line(source[['datetime', 'voltage_measured']].resample('5h', on = 'datetime').mean().reset_index(), x = 'datetime', y = 'voltage_measured', title='Average Measured Voltage Across Battery Lifetime')
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig6 = px.line(sourceCapacity, x = 'cycle', y = 'capacity', title='Capacity of Battery Againt Cycle')
    fig6.update_traces(line_color='red', line_width=3)
    st.plotly_chart(fig6, use_container_width=True)
with col2:
    fig7 = px.line(sourceCapacity[['datetime', 'capacity']].resample('12h', on='datetime').mean().reset_index(), x = 'datetime', y = 'capacity', title='Capacity of Battery Againt Time')
    fig7.update_traces(line_color='red', line_width=3)
    st.plotly_chart(fig7, use_container_width=True)

st.markdown("<h4 style='text-align: center;'>Measuring Performance Across Cycles</h4>", unsafe_allow_html=True)


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


