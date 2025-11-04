# Focus on layout, filters, and visuals HERE

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


from campaign_metric_explorer import load_data, compute_metrics


import streamlit as st 
import plotly.express as px 
from src.campaign_metric_explorer import load_data, compute_metrics 

st.set_page_config(page_title='Campaign Metric Explorer', layout='wide')
st.markdown(
    """
    <style>
    body {
        background-color: #E9F0EF;
    }

    /* Main header */
    .header-bar {
        background-color: #111827;
        padding: 12px 24px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* Metric cards */
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border-top: 5px solid #FF8C66;
        margin-bottom: 15px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 4px;
    }

    .metric-label {
        font-size: 14px;
        font-weight: 500;
        color: #6B7280;
        letter-spacing: 0.5px;
    }

    /* Section headers */
    h3 {
        color: #1F2937;
        font-weight: 700;
    }

    hr {
        border: 0;
        height: 1px;
        background: #D1D5DB;
        margin: 1.5rem 0;
    }

    /* Chart background */
    .chart-container {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load + process data
df = load_data('/Users/kevineddy/Desktop/AI_Data_Projects/campaign-metric-explorer/data/simulated_campaign_data.csv')
df = compute_metrics(df) 
df = df.sort_values(by='Date', ascending=True)

# Sidebar filters
st.sidebar.header('Filter Data')
channels = st.sidebar.multiselect('Select Channel(s)', df['Channel'].unique())
if channels:
    df = df[df['Channel'].isin(channels)]

# Sidebar Section
st.markdown("<div class='header-bar'><h2>Campaign Performance Dashboard</h2></div>", unsafe_allow_html=True)

# TOP ROW: IMPRESSIONS, CLICKS, CONVERSIONS
#st.markdown('Top Campaign Performance Metrics')
st.markdown("### Engagement Overview")
top_col1, top_col2, top_col3 = st.columns(3)

with top_col1:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{df['Impressions'].sum():,}</div>
            <div class='metric-label'>Impressions</div>
        </div>
    """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{df['Clicks'].sum():,}</div>
            <div class='metric-label'>Clicks</div>
        </div>
    """, unsafe_allow_html=True)

with top_col3:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{df['Conversions'].sum():,}</div>
            <div class='metric-label'>Conversions</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# MIDDLE SECTION: LEFT (SPEND, REVENUE, ROAS) / RIGHT (ROAS CHART)
left_col, right_col = st.columns([1, 2], gap="large")

# Main Visual Area - Spend & Revenue (Left) + ROAS Graph (Right)
left_col, right_col = st.columns([1,2], gap='large')

with left_col:
    st.markdown("### 💰 Financial Overview")
    total_spend = df["Spend"].sum()
    total_revenue = df["Revenue"].sum()
    total_roas = total_revenue / total_spend if total_spend > 0 else 0

    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>${total_spend:,.0f}</div>
            <div class='metric-label'>Total Spend</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>${total_revenue:,.0f}</div>
            <div class='metric-label'>Total Revenue</div>
        </div>
        <div class='metric-card'>
            <div class='metric-value'>{total_roas:.2f}x</div>
            <div class='metric-label'>Overall ROAS</div>
        </div>
    """, unsafe_allow_html=True)

with right_col:
    st.markdown("### 📈 ROAS Over Time by Channel")
    fig_roas = px.line(
        df,
        x="Date",
        y="ROAS",
        color="Channel",
        title="ROAS Trend",
        labels={"ROAS": "Return on Ad Spend", "Date": "Date"},
        template="plotly_white"
    )
    fig_roas.update_traces(line=dict(width=3))
    fig_roas.update_layout(
        plot_bgcolor="#F9FAFB",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#111827")
    )
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.plotly_chart(fig_roas, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)



# BOTTOM ROW - CTR GRAPH
st.markdown("### CTR Over Time by Channel")
fig_ctr = px.line(
    df,
    x="Date",
    y="CTR",
    color="Channel",
    title="CTR Trend",
    labels={"CTR": "Click-Through Rate", "Date": "Date"},
    template="plotly_white"
)
fig_ctr.update_traces(line=dict(width=3))
fig_ctr.update_layout(
    plot_bgcolor="#F9FAFB",
    paper_bgcolor="#FFFFFF",
    font=dict(color="#111827")
)
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.plotly_chart(fig_ctr, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)



# Chart
#fig = px.line(df, x='Date', y='ROAS', color='Channel', title='ROAS Over Time', height=600)
#st.plotly_chart(fig, use_container_width=True)




