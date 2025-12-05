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
# MINIMAL SAFE CSS - ONLY FIXES DROPDOWN TEXT, NOTHING ELSE
# ==================================================================================
st.markdown("""
<style>
/* ONLY fix dropdown option text color */
div[data-baseweb="select"] [role="option"] {
    color: #1f1f1f !important;
}

/* ONLY fix multiselect option text */
div[data-baseweb="select"] li[role="option"] {
    color: #1f1f1f !important;
}

/* ONLY fix dropdown selected value text */
div[data-baseweb="select"] > div:first-child {
    color: #1f1f1f !important;
}

/* ONLY fix button text */
button {
    color: #1f1f1f !important;
}

button:hover {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END MINIMAL CSS
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