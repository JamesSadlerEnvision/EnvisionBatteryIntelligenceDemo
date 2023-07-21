import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Trading Optimisations</h1>", unsafe_allow_html=True)

#@st.cache_data
def load_data():
    trading = pd.read_csv('data/trading.csv', parse_dates=['DATE_time'])
    
    return trading

trading = load_data()
trading['datetime'] = pd.date_range(pd.Timestamp.now(), freq = '1H', periods = len(trading))

st.markdown("<h3 style='text-align: center;'>Key Metrics</h3>", unsafe_allow_html=True)  

col1, col2, col3 = st.columns(3)


with col1:
    st.metric("Projected Profit", f"£402.2", "4.5%")

with col2:
    st.metric("Current Charge/Discharge State", f"Rest", "0 C")
    
with col3:
    st.metric("System SOC", f"0 %", )


fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=trading.datetime[:48], y=trading['WEP ($/MWh)'][:48],
                    mode='lines',
                    name='prices'))
fig.add_trace(go.Scatter(x=trading.datetime[:48], y=trading['SOC'][:48],
                    mode='lines',
                    name='SOC',
                    line_color = 'red'),
                    secondary_y = True)
fig.update_xaxes(title_text="Datetime")
fig.update_yaxes(title_text="<b>Spot Price</b> $", secondary_y=False)
fig.update_yaxes(title_text="<b>Recommended SOC</b> %", secondary_y=True)
st.plotly_chart(fig, use_container_width=True)
