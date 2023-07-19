import streamlit as st
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Health Manager POC Experiment</h1>", unsafe_allow_html=True)

#@st.cache_data
def load_data():
    df = pd.read_csv('data/DemoBatteryData.csv', index_col = 0, parse_dates = ['datetime'])
    capacity_df = pd.read_csv('data/DemoCapacityData.csv', index_col = 0, parse_dates = ['datetime'])
    
    return df, capacity_df

df, capacity_df = load_data()
capacity_df = capacity_df[capacity_df.battery.isin(['B0005', 'B0006', 'B0007'])]


#@st.cache_data
def pivot_capacity(capacity_df):
    capacity_pivot = capacity_df.pivot(index = 'datetime', columns = 'battery', values = 'capacity')
    total_capacity_og = capacity_pivot.iloc[0].sum()
    capacity_pivot['Total'] = capacity_pivot.sum(axis = 1)
    capacity_pivot['Total SOH'] = 100*capacity_pivot['Total'] / total_capacity_og

    return capacity_pivot


capacity_pivot = pivot_capacity(capacity_df)

st.markdown("<h3 style='text-align: center;'>System Aging Analysis</h3>", unsafe_allow_html=True)

with st.container():
    fig = px.area(capacity_pivot, y = 'Total SOH')
    fig.update_layout(title_text='Total System SOH', title_x=0.45)
    fig.add_hline(y=70, line_color = 'red', line_dash = 'dash')
    fig.update_layout(yaxis_range=[60, 110])
    st.plotly_chart(fig, use_container_width=True)


batteries = st.multiselect(
    'Battery:',
    ['B0005', 'B0006', 'B0007'],
    default = 'B0005'
    )
source = capacity_pivot[capacity_pivot.columns.intersection(batteries)]


# Now determine SOH by battery. First calculate og capacity and then merge
# to get SOH per og_capacity throughout lifetime
og_capacities = capacity_df[['battery','capacity']].groupby('battery').nth(0)
og_capacities = og_capacities.rename(columns = {'capacity': 'og_capacity'})
capacity_df = capacity_df.merge(og_capacities)
capacity_df = capacity_df[capacity_df.battery.isin(batteries)]

capacity_df['SOH'] = 100*capacity_df['capacity'] / capacity_df['og_capacity']


col1, col2 = st.columns(2)

with col1:
    fig2 = px.line(capacity_df, x="datetime", y="SOH", color='battery')
    fig2.update_layout(title_text='Module SOH', title_x=0.5)
    st.plotly_chart(fig2, use_container_width=True)


with col2:
    fig3 = px.line(capacity_df, x="cycle", y="SOH", color='battery')
    fig3.update_layout(title_text='Module SOH', title_x=0.5)
    st.plotly_chart(fig3, use_container_width=True)

