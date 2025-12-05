"""
CloudIDP Enhanced v2.0 - Enterprise Multi-Account Cloud Infrastructure Development Platform
Simple Blue Theme - Clean & Professional
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from config_settings import AppConfig
from core_session_manager import SessionManager
from components_navigation import Navigation
from components_sidebar import GlobalSidebar

# Page configuration
st.set_page_config(
    page_title="CloudIDP Enhanced v2.0",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================================================
# SIMPLE BLUE THEME - CLEAN & PROFESSIONAL
# ==================================================================================
st.markdown("""
<style>
/* ===== GLOBAL THEME ===== */
:root {
    --primary-color: #2E86DE;
    --secondary-color: #0652DD;
    --background-color: #FFFFFF;
    --text-color: #000000;
    --border-color: #E0E0E0;
}

/* Main app background - WHITE */
.main {
    background-color: white !important;
}

/* All text - BLACK */
body, p, span, div, label, h1, h2, h3, h4, h5, h6 {
    color: black !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #F5F7FA !important;
}

[data-testid="stSidebar"] * {
    color: black !important;
}

/* ===== HEADERS ===== */
h1, h2, h3 {
    color: #2E86DE !important;
}

/* ===== BUTTONS ===== */
button {
    background-color: #2E86DE !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 8px 16px !important;
    font-weight: 500 !important;
}

button:hover {
    background-color: #0652DD !important;
    color: white !important;
}

/* ===== DROPDOWNS & SELECTS ===== */
/* Dropdown labels */
.stSelectbox label,
.stMultiSelect label,
.stTextInput label,
.stNumberInput label,
.stTextArea label {
    color: black !important;
    font-weight: 500 !important;
}

/* Dropdown options text - BLACK */
div[data-baseweb="select"] [role="option"],
div[data-baseweb="select"] li,
[role="option"] {
    color: black !important;
    background-color: white !important;
}

/* Dropdown selected value - BLACK */
div[data-baseweb="select"] > div {
    color: black !important;
    background-color: white !important;
}

/* Multiselect tags */
div[data-baseweb="tag"] {
    background-color: #2E86DE !important;
}

div[data-baseweb="tag"] span {
    color: white !important;
}

/* ===== INPUT FIELDS ===== */
input, textarea {
    background-color: white !important;
    color: black !important;
    border: 1px solid #E0E0E0 !important;
}

/* ===== TABS ===== */
.stTabs [data-baseweb="tab-list"] {
    background-color: white !important;
}

.stTabs [data-baseweb="tab"] {
    color: black !important;
}

.stTabs [aria-selected="true"] {
    color: #2E86DE !important;
    border-bottom: 2px solid #2E86DE !important;
}

/* ===== METRICS ===== */
[data-testid="stMetricLabel"] {
    color: black !important;
}

[data-testid="stMetricValue"] {
    color: #2E86DE !important;
}

/* ===== INFO/WARNING/ERROR BOXES ===== */
.stAlert {
    background-color: white !important;
    border-left: 4px solid #2E86DE !important;
}

/* ===== DATAFRAMES ===== */
.stDataFrame {
    background-color: white !important;
}

table {
    background-color: white !important;
}

th {
    background-color: #2E86DE !important;
    color: white !important;
}

td {
    color: black !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader {
    background-color: #F5F7FA !important;
    color: black !important;
}

/* ===== RADIO & CHECKBOX ===== */
.stRadio label,
.stCheckbox label {
    color: black !important;
}

/* ===== CLEAN BORDERS ===== */
.stSelectbox > div,
.stMultiSelect > div,
.stTextInput > div,
.stNumberInput > div {
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END SIMPLE BLUE THEME
# ==================================================================================

# Simple header
st.markdown("""
<div style="background: linear-gradient(135deg, #2E86DE 0%, #0652DD 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0;">☁️ CloudIDP Enhanced v2.0</h1>
    <p style="color: white; margin: 5px 0 0 0; opacity: 0.9;">Enterprise Multi-Account Cloud Infrastructure Development Platform</p>
</div>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Initialize session
    SessionManager.initialize()
    
    # Render global sidebar
    GlobalSidebar.render()
    
    # Render main navigation
    Navigation.render()
    
    # Simple footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        st.caption(f"🔗 Connected Accounts: {SessionManager.get_active_account_count()}")
    with col3:
        st.caption("☁️ CloudIDP Enhanced v2.0")

if __name__ == "__main__":
    main()