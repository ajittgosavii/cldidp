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

# ===== GLOBAL CSS FIX FOR BUTTON VISIBILITY =====
st.markdown("""
<style>
/* Make all button text visible across entire app */
.stButton > button {
    color: #1f1f1f !important;
    font-weight: 600 !important;
    background-color: white !important;
    border: 2px solid #667eea !important;
}
.stButton > button:hover {
    background-color: #667eea !important;
    color: white !important;
    border: 2px solid #667eea !important;
}

/* Primary button styling */
.stButton > button[kind="primary"] {
    background-color: #667eea !important;
    color: white !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background-color: #5568d3 !important;
}

/* Secondary button styling */
.stButton > button[kind="secondary"] {
    color: #1f1f1f !important;
    background-color: white !important;
    border: 2px solid #667eea !important;
}
.stButton > button[kind="secondary"]:hover {
    background-color: #f0f0f0 !important;
}
</style>
""", unsafe_allow_html=True)
# ===== END GLOBAL CSS FIX =====

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