import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Safety Manager POC Experiment</h1>", unsafe_allow_html=True)

df = pd.read_csv('data/DemoBatteryData.csv', index_col = 0, parse_dates = ['datetime'])
soc_df = pd.read_csv('data/SOC_Data.csv', index_col = 0, parse_dates = ['datetime'])
safety_df = pd.read_csv('data/safety_data.csv')
temp_df = pd.read_csv('data/temp_data.csv')

fig = px.line(soc_df, x = 'datetime', y = 'SOC')
fig.update_layout(title_text='System SOC', title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<h3 style='text-align: center;'>Alerts</h3>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h5 style='text-align: center;'>System Alert Descriptions</h5>", unsafe_allow_html=True)  
    st.dataframe(safety_df, use_container_width=True)

with col2:
    st.markdown("<h5 style='text-align: center;'>Safety Alerts Volume</h5>", unsafe_allow_html=True) 
    color_discrete_map = {'Good': 'green', 'Warning': 'goldenrod', 'Severe':'red'}
    fig2 = px.histogram(safety_df, x= 'State', color = 'State',color_discrete_map = color_discrete_map)
    fig2.update_xaxes(categoryorder='array', categoryarray= ['Good', 'Warning', 'Severe'])
    st.plotly_chart(fig2, use_container_width=True)


st.markdown("<h5 style='text-align: center;'>System Temperature</h5>", unsafe_allow_html=True) 

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=temp_df.datetime, y=temp_df.Temp3pm,
                    mode='lines',
                    name='temperature'))
fig4.add_trace(go.Scatter(x=temp_df[temp_df.Temp3pm > 32].datetime, y=temp_df[temp_df.Temp3pm > 32].Temp3pm,
                    mode='markers',
                    name='anomalies',
                    marker = {'color' : 'red'}))
st.plotly_chart(fig4, use_container_width=True)
