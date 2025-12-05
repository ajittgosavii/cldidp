"""
CloudIDP Enhanced v2.0 - Enterprise Multi-Account Cloud Infrastructure Development Platform
Multi-Account | Multi-Region | Real-Time AWS Integration | AWS-Themed UI
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
from aws_theme import AWSTheme

# Page configuration
st.set_page_config(
    page_title="CloudIDP Enhanced v2.0 - AWS Cloud Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply AWS Theme
AWSTheme.apply_aws_theme()

# ==================================================================================
# GLOBAL CSS FIX FOR DROPDOWN TEXT VISIBILITY - APPLIES TO ENTIRE APPLICATION
# ==================================================================================
st.markdown("""
<style>
/* ===== DROPDOWN & SELECT MENUS ===== */
/* Fix for all Streamlit selectbox dropdowns */
.stSelectbox label,
.stSelectbox label *,
.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="select"] *,
.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] div,
div[data-baseweb="select"],
div[data-baseweb="select"] *,
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
div[data-baseweb="select"] > div,
div[role="button"][aria-haspopup="listbox"],
div[role="button"][aria-haspopup="listbox"] *,
div[role="button"][aria-haspopup="listbox"] span,
[role="option"],
[role="option"] *,
[role="option"] span,
[role="option"] div,
li[role="option"],
li[role="option"] *,
li[role="option"] span,
ul[role="listbox"] li,
ul[role="listbox"] li *,
ul[role="listbox"] li span {
    color: #1f1f1f !important;
    font-weight: 400 !important;
}

/* Dropdown label text */
.stSelectbox > label,
.stSelectbox > label > div,
.stSelectbox > label > div > p {
    color: #f0f0f0 !important;
}

/* Selected value in dropdown */
.stSelectbox div[data-baseweb="select"] > div:first-child,
.stSelectbox div[data-baseweb="select"] > div:first-child * {
    color: #1f1f1f !important;
}

/* ===== MULTISELECT MENUS ===== */
.stMultiSelect label,
.stMultiSelect label *,
.stMultiSelect div[data-baseweb="select"],
.stMultiSelect div[data-baseweb="select"] *,
.stMultiSelect div span,
div[data-baseweb="tag"],
div[data-baseweb="tag"] *,
div[data-baseweb="tag"] span {
    color: #1f1f1f !important;
}

/* Multiselect label */
.stMultiSelect > label {
    color: #f0f0f0 !important;
}

/* Selected tags in multiselect */
div[data-baseweb="tag"] {
    background-color: #667eea !important;
}

div[data-baseweb="tag"] span {
    color: white !important;
}

/* ===== RADIO BUTTONS ===== */
.stRadio label,
.stRadio label *,
.stRadio div[role="radiogroup"],
.stRadio div[role="radiogroup"] *,
.stRadio div[role="radiogroup"] label,
.stRadio div[role="radiogroup"] label * {
    color: #f0f0f0 !important;
}

/* ===== TEXT INPUTS ===== */
.stTextInput label,
.stTextInput label *,
.stTextArea label,
.stTextArea label *,
.stNumberInput label,
.stNumberInput label * {
    color: #f0f0f0 !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    color: #1f1f1f !important;
    background-color: white !important;
}

/* ===== CHECKBOXES ===== */
.stCheckbox label,
.stCheckbox label *,
.stCheckbox span {
    color: #f0f0f0 !important;
}

/* ===== TIME & DATE INPUTS ===== */
.stTimeInput label,
.stTimeInput label *,
.stDateInput label,
.stDateInput label * {
    color: #f0f0f0 !important;
}

.stTimeInput input,
.stDateInput input {
    color: #1f1f1f !important;
    background-color: white !important;
}

/* ===== SLIDER LABELS ===== */
.stSlider label,
.stSlider label * {
    color: #f0f0f0 !important;
}

/* ===== BUTTONS ===== */
button,
button * {
    color: #1f1f1f !important;
    font-weight: 600 !important;
}

button {
    background-color: white !important;
    border: 2px solid #667eea !important;
}

button:hover {
    background-color: #667eea !important;
}

button:hover,
button:hover * {
    color: white !important;
}

button[kind="primary"] {
    background-color: #667eea !important;
    color: white !important;
    border: none !important;
}

button[kind="primary"] * {
    color: white !important;
}

button[kind="primary"]:hover {
    background-color: #5568d3 !important;
}

/* ===== EXPANDERS ===== */
.streamlit-expanderHeader,
.streamlit-expanderHeader *,
.streamlit-expanderContent,
.streamlit-expanderContent * {
    color: inherit !important;
}

/* ===== DATAFRAMES & TABLES ===== */
.stDataFrame,
.stDataFrame *,
table,
table *,
thead,
thead *,
tbody,
tbody *,
th,
td {
    color: #1f1f1f !important;
}

/* ===== METRICS ===== */
.stMetric label,
.stMetric label *,
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {
    color: #f0f0f0 !important;
}

/* ===== INFO/WARNING/ERROR BOXES ===== */
.stAlert,
.stAlert * {
    color: inherit !important;
}

/* ===== ENSURE VISIBILITY ===== */
* {
    visibility: visible !important;
    opacity: 1 !important;
}

/* Don't hide any text */
span,
div,
p,
label {
    display: block !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END GLOBAL CSS FIX
# ==================================================================================

def main():
    """Main application entry point"""
    
    # Initialize session
    SessionManager.initialize()
    
    # Render AWS-themed header
    AWSTheme.aws_header(
        "CloudIDP Enhanced v2.0",
        "Enterprise Multi-Account Cloud Infrastructure Development Platform | Powered by AWS"
    )
    
    # Render global sidebar
    GlobalSidebar.render()
    
    # Render main navigation
    Navigation.render()
    
    # AWS-themed footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        st.caption(f"🔗 Connected Accounts: {SessionManager.get_active_account_count()}")
    with col3:
        st.caption("🚀 CloudIDP Enhanced v2.0 - AWS Edition")

if __name__ == "__main__":
    main()