# Focus on layout, filters, and visuals HERE

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


from campaign_metric_explorer import load_data, compute_metrics


import streamlit as st 
import plotly.express as px 
from src.campaign_metric_explorer import load_data, compute_metrics 

st.set_page_config(page_title='Campaign Metric Explorer', layout='wide')
st.title('Camopaign Metric Explorer')

# Load + process data
df = load_data('/Users/kevineddy/Desktop/AI_Data_Projects/campaign-metric-explorer/data/simulated_campaign_data.csv')
df = compute_metrics(df) 
df = df.sort_values(by='Date', ascending=True)

# Sidebar filters
channels = st.sidebar.multiselect('Select Channel', df['Channel'].unique())
if channels:
    df = df[df['Channel'].isin(channels)]

# Metrics
st.metric('Average CTR', f"{df['CTR'].mean():.2%}")
st.metric("Average CVR", f"{df['CVR'].mean():.2%}")
st.metric("Average ROAS", f"{df['ROAS'].mean():.2f}")

# Chart
fig = px.line(df, x='Date', y='ROAS', color='Channel', title='ROAS Over Time', height=600)
st.plotly_chart(fig, use_container_width=True)




