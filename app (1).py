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

# ========== CUSTOM STYLING ==========
st.markdown(
    """
    <style>
        .main-header {
            font-size: 2.8rem;
            color: #2E86C1;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .section-header {
            font-size: 1.8rem;
            color: #1A5276;
            border-left: 5px solid #3498DB;
            padding-left: 15px;
            margin-top: 30px;
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== TITLE ==========
st.markdown('<h1 class="main-header">📈 MARKETING CAMPAIGN ANALYTICS DASHBOARD</h1>', unsafe_allow_html=True)
st.markdown("---")

# ========== DATA LOADING SECTION ==========
@st.cache_data
def load_data():
    """Load Excel data with multiple fallback methods"""
    try:
        # METHOD 1: Try with space in filename
        df = pd.read_excel('Final_Marketing Team Data.xlsx', sheet_name='Marketing_Team_Data')
        st.sidebar.success("✅ Data loaded from local file")
        return df
    except:
        try:
            # METHOD 2: Try without space (underscore)
            df = pd.read_excel('Final_Marketing_Team_Data.xlsx', sheet_name='Marketing_Team_Data')
            st.sidebar.success("✅ Data loaded from local file")
            return df
        except:
            try:
                # METHOD 3: Try different sheet names
                sheet_names = ['Marketing_Team_Data', 'Sheet1', 'Data', 'Marketing']
                for sheet in sheet_names:
                    try:
                        df = pd.read_excel('Final_Marketing Team Data.xlsx', sheet_name=sheet)
                        st.sidebar.success(f"✅ Data loaded from sheet: {sheet}")
                        return df
                    except:
                        continue
            except:
                pass

    # METHOD 4: File uploader as final fallback
    st.sidebar.warning("⚠️ File not found. Please upload manually")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Excel File",
        type=['xlsx'],
        help="Upload your marketing data Excel file"
    )
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file, sheet_name='Marketing_Team_Data')
            st.sidebar.success("✅ File uploaded successfully")
            return df
        except:
            try:
                df = pd.read_excel(uploaded_file, sheet_name=0)  # Try first sheet
                st.sidebar.success("✅ File uploaded (first sheet)")
                return df
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")
                return None
    return None

# ========== SIDEBAR ==========
with st.sidebar:
    st.title("🔧 CONTROL PANEL")
    st.markdown("---")

    # Data info
    st.subheader("📁 Data Information")
    st.info("""
    **Expected File:** Final_Marketing Team Data.xlsx
    **Expected Sheet:** Marketing_Team_Data
    """)

    # Filters (will be populated after data loads)
    st.markdown("---")
    st.subheader("🎯 Filters")
    st.write("*Filters will appear after data loads*")

# ========== LOAD DATA ==========
data_load_state = st.empty()
data_load_state.text("🔄 Loading data...")
df = load_data()
data_load_state.empty()

# ========== MAIN DASHBOARD ==========
if df is not None and not df.empty:
    # Show success message
    st.success(f"✅ Data loaded successfully! {len(df)} records found")

    # Clean column names (remove special characters, spaces, make lowercase)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    # Show column names for debugging
    st.write(f"**Available Columns:** {', '.join(df.columns.tolist()[:8])}...")

    # ========== TOP KPI METRICS ==========
    st.markdown("### 📊 KEY PERFORMANCE INDICATORS")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        try:
            # Try different possible column names for spend
            spend_columns = ['amount_spent_in_inr', 'amount_spent', 'spent', 'spent_inr', 'cost']
            for col in spend_columns:
                if col in df.columns:
                    total_spent = df[col].sum()
                    st.metric("💰 Total Spend", f"₹{total_spent:,.0f}")
                    break
            else:
                st.metric("💰 Total Spend", "Column not found")
        except:
            st.metric("💰 Total Spend", "₹0")

    with col2:
        try:
            if 'clicks' in df.columns:
                total_clicks = df['clicks'].sum()
                st.metric("🖱️ Total Clicks", f"{total_clicks:,}")
            else:
                st.metric("🖱️ Total Clicks", "Column not found")
        except:
            st.metric("🖱️ Total Clicks", "0")

    with col3:
        try:
            if 'impressions' in df.columns:
                total_impressions = df['impressions'].sum()
                st.metric("👁️ Total Impressions", f"{total_impressions:,}")
            else:
                st.metric("👁️ Total Impressions", "Column not found")
        except:
            st.metric("👁️ Total Impressions", "0")

    with col4:
        try:
            if 'clicks' in df.columns and 'impressions' in df.columns:
                if df['impressions'].sum() > 0:
                    avg_ctr = (df['clicks'].sum() / df['impressions'].sum()) * 100
                    st.metric("📈 Avg CTR", f"{avg_ctr:.2f}%")
                else:
                    st.metric("📈 Avg CTR", "0%")
            else:
                st.metric("📈 Avg CTR", "Data missing")
        except:
            st.metric("📈 Avg CTR", "0%")

    st.markdown("---")

    # ========== FILTERS IN SIDEBAR (now that we have data) ==========
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎯 Apply Filters")

        # Campaign filter
        campaign_cols = [col for col in df.columns if 'campaign' in col.lower()]
        if campaign_cols:
            campaign_col = campaign_cols[0]
            campaigns = ['All'] + sorted(df[campaign_col].dropna().unique().tolist())
            selected_campaign = st.selectbox("Select Campaign", campaigns)
        else:
            selected_campaign = 'All'
            st.write("No campaign column found")

        # Audience filter
        audience_cols = [col for col in df.columns if 'audience' in col.lower()]
        if audience_cols:
            audience_col = audience_cols[0]
            audiences = ['All'] + sorted(df[audience_col].dropna().unique().tolist())
            selected_audience = st.selectbox("Select Audience", audiences)
        else:
            selected_audience = 'All'

        # Age filter
        age_cols = [col for col in df.columns if 'age' in col.lower()]
        if age_cols:
            age_col = age_cols[0]
            ages = ['All'] + sorted(df[age_col].dropna().unique().tolist())
            selected_age = st.selectbox("Select Age Group", ages)
        else:
            selected_age = 'All'

    # Apply filters
    filtered_df = df.copy()
    if selected_campaign != 'All' and campaign_cols:
        filtered_df = filtered_df[filtered_df[campaign_col] == selected_campaign]
    if selected_audience != 'All' and audience_cols:
        filtered_df = filtered_df[filtered_df[audience_col] == selected_audience]
    if selected_age != 'All' and age_cols:
        filtered_df = filtered_df[filtered_df[age_col] == selected_age]

    # ========== VISUALIZATION SECTION ==========
    st.markdown("### 📈 PERFORMANCE ANALYTICS")

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Campaign Performance", "👥 Audience Insights", "🌍 Geographic Analysis", "📋 Raw Data"])

    with tab1:
        st.subheader("Campaign Performance")

        # Chart 1: Basic bar chart of clicks by campaign
        if campaign_cols and 'clicks' in df.columns:
            campaign_data = filtered_df.groupby(campaign_col)['clicks'].sum().reset_index()
            campaign_data = campaign_data.sort_values('clicks', ascending=False).head(10)

            fig1 = px.bar(
                campaign_data,
                x=campaign_col,
                y='clicks',
                title='Top 10 Campaigns by Clicks',
                labels={'clicks': 'Total Clicks', campaign_col: 'Campaign'},
                color='clicks',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Spend vs Clicks scatter
        spend_cols = [col for col in df.columns if 'spent' in col.lower() or 'cost' in col.lower() or 'amount' in col.lower()]
        if campaign_cols and 'clicks' in df.columns and spend_cols:
            spend_col = spend_cols[0]
            scatter_data = filtered_df.groupby(campaign_col).agg({
                'clicks': 'sum',
                spend_col: 'sum'
            }).reset_index()

            fig2 = px.scatter(
                scatter_data,
                x=spend_col,
                y='clicks',
                size='clicks',
                color=campaign_col,
                hover_name=campaign_col,
                title='Campaign Efficiency: Spend vs Clicks',
                labels={'clicks': 'Total Clicks', spend_col: 'Total Spend'}
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("Audience Insights")

        col1, col2 = st.columns(2)

        with col1:
            if audience_cols and 'clicks' in df.columns:
                audience_data = filtered_df.groupby(audience_col)['clicks'].sum().reset_index()

                fig3 = px.pie(
                    audience_data,
                    values='clicks',
                    names=audience_col,
                    title='Clicks Distribution by Audience',
                    hole=0.3
                )
                st.plotly_chart(fig3, use_container_width=True)

        with col2:
            if audience_cols and spend_cols:
                spend_col = spend_cols[0]
                # ... rest of the code for the second chart in tab2
                # For now, just a placeholder
                st.warning("Further audience analysis visualization can go here.")

    with tab3:
        st.subheader("Geographic Analysis")

        geo_cols = [col for col in df.columns if 'country' in col.lower() or 'region' in col.lower()]
        if geo_cols and 'clicks' in df.columns:
            geo_col = geo_cols[0]
            geo_data = filtered_df.groupby(geo_col)['clicks'].sum().reset_index()

            fig_geo = px.choropleth(
                geo_data,
                locations=geo_col,
                locationmode='country names',
                color='clicks',
                hover_name=geo_col,
                color_continuous_scale="Plasma",
                title='Clicks by Country'
            )
            st.plotly_chart(fig_geo, use_container_width=True)
        else:
            st.info("No geographic columns found for analysis.")


    with tab4:
        st.subheader("Raw Data")
        st.dataframe(filtered_df)


elif df is None:
    st.warning("Please upload an Excel file to get started.")
else:
    st.warning("The loaded dataframe is empty. Please check your data or filters.")



# Footer
st.markdown("""
--- 
Created with ❤️ by Arafat Hossain
""")

