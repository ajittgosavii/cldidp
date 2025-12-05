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

# ===== NUCLEAR OPTION: FORCE BUTTON TEXT VISIBILITY =====
st.markdown("""
<style>
/* NUCLEAR: Override EVERYTHING to force black text on white buttons */
button,
button *,
button span,
button div,
.stButton button,
.stButton button *,
.stButton button span,
.stButton button div,
div[data-testid="stButton"] button,
div[data-testid="stButton"] button *,
div[data-testid="stButton"] button span,
div[data-testid="stButton"] button div,
button[data-baseweb="button"],
button[data-baseweb="button"] *,
button[data-baseweb="button"] span,
button[data-baseweb="button"] div {
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Force button backgrounds to be white */
button,
.stButton button,
div[data-testid="stButton"] button,
button[data-baseweb="button"] {
    background-color: #ffffff !important;
    border: 2px solid #667eea !important;
}

/* Hover state - purple background, white text */
button:hover,
button:hover *,
button:hover span,
button:hover div,
.stButton button:hover,
.stButton button:hover *,
div[data-testid="stButton"] button:hover,
div[data-testid="stButton"] button:hover *,
button[data-baseweb="button"]:hover,
button[data-baseweb="button"]:hover * {
    color: #ffffff !important;
    background-color: #667eea !important;
}

/* Primary buttons - purple background, white text always */
button[kind="primary"],
button[kind="primary"] *,
button[kind="primary"] span,
button[kind="primary"] div {
    background-color: #667eea !important;
    color: #ffffff !important;
    border: none !important;
}

button[kind="primary"]:hover {
    background-color: #5568d3 !important;
}

/* Force visibility of ALL text elements */
* {
    visibility: visible !important;
}

/* Override any display:none on text */
button span,
button div,
.stButton button span,
.stButton button div {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)
# ===== END NUCLEAR OPTION =====

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
