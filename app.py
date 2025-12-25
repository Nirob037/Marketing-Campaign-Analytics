
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Marketing Campaign Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
    }
</style>
""", unsafe_allow_html=True)

# ========== TITLE ==========
st.markdown('<h1 class="main-header">📈 Marketing Campaign Analytics Dashboard</h1>', unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("🔧 Navigation")
    page = st.radio(
        "Select Page",
        ["Overview", "Campaign Analysis", "Geographic View", "Audience Insights"]
    )
    
    st.markdown("---")
    st.title("⚙️ Data Controls")
    
    # File uploader for data
    uploaded_file = st.file_uploader("Upload Excel File", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        data_load_state = st.text('Loading data...')
        df = pd.read_excel(uploaded_file, sheet_name='Marketing_Team_Data')
        data_load_state.text('Data loaded successfully!')
        st.session_state['df'] = df
    else:
        st.warning("Please upload your Excel file to begin analysis")
        # Create a dummy dataframe for demonstration
        df = pd.DataFrame({
            'campaign ID': ['Campaign 1', 'Campaign 2'],
            'Campaign Name': ['Test 1', 'Test 2'],
            'Audience': ['Students', 'Educators'],
            'Clicks': [100, 150],
            'Amount Spent in INR': [1000, 1500],
            'Geography': ['India', 'USA']
        })
        st.session_state['df'] = df

# ========== MAIN DASHBOARD ==========
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Display basic info about the data
    st.subheader("📋 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if 'campaign ID' in df.columns:
            st.metric("Total Campaigns", df['campaign ID'].nunique())
        else:
            st.metric("Total Rows", len(df))
    
    with col2:
        if 'Clicks' in df.columns:
            st.metric("Total Clicks", f"{df['Clicks'].sum():,}")
        else:
            st.metric("Data Columns", len(df.columns))
    
    with col3:
        if 'Amount Spent in INR' in df.columns:
            total_spent = df['Amount Spent in INR'].sum()
            st.metric("Total Spent", f"₹{total_spent:,.0f}")
    
    with col4:
        if 'Impressions' in df.columns:
            st.metric("Total Impressions", f"{df['Impressions'].sum():,}")
    
    # Show data preview
    st.subheader("📊 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    
    # ========== PAGE CONTENT BASED ON SELECTION ==========
    if page == "Overview":
        st.subheader("📈 Campaign Performance Overview")
        
        # Example chart 1: Clicks by Campaign
        if 'Clicks' in df.columns and 'Campaign Name' in df.columns:
            fig1 = px.bar(
                df.groupby('Campaign Name')['Clicks'].sum().reset_index(),
                x='Campaign Name',
                y='Clicks',
                title='Total Clicks by Campaign',
                color='Clicks',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        # Example chart 2: Spend by Geography
        if 'Amount Spent in INR' in df.columns and 'Geography' in df.columns:
            fig2 = px.pie(
                df.groupby('Geography')['Amount Spent in INR'].sum().reset_index(),
                values='Amount Spent in INR',
                names='Geography',
                title='Spend Distribution by Geography'
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    elif page == "Campaign Analysis":
        st.subheader("🎯 Detailed Campaign Analysis")
        
        # Add your campaign analysis code here
        st.write("Campaign analysis features will be added here.")
        
    elif page == "Geographic View":
        st.subheader("🌍 Geographic Performance")
        
        # Add geographic analysis code here
        st.write("Geographic analysis features will be added here.")
        
    elif page == "Audience Insights":
        st.subheader("👥 Audience Insights")
        
        # Add audience analysis code here
        st.write("Audience analysis features will be added here.")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("📊 *Marketing Campaign Analytics Dashboard v1.0*")
