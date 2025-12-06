"""
Cloud Infrastructure Development Platform
COMPATIBLE WITH NEW AWS THEME - No CSS conflicts
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
    page_title="Cloud Infrastructure Development Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================================================
# MINIMAL CSS - COMPATIBLE WITH AWS THEME
# No CSS that interferes with metric cards!
# ==================================================================================
st.markdown("""
<style>
/* Minimal CSS that doesn't conflict with aws_theme.py */

/* Ensure main background doesn't override */
.main {
    background-color: transparent !important;
}

/* Let aws_theme.py handle all styling */
</style>
""", unsafe_allow_html=True)
# ==================================================================================
# END MINIMAL CSS
# ==================================================================================

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #FF9900 0%, #EC7211 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; box-shadow: 0 4px 8px rgba(255, 153, 0, 0.3);">
    <h1 style="color: #232F3E !important; margin: 0; font-weight: 700;">☁️ Cloud Infrastructure Development Platform</h1>
    <p style="color: #232F3E !important; margin: 5px 0 0 0; font-size: 16px; font-weight: 600;">Enterprise Multi-Account Cloud Management</p>
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
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        st.caption(f"🔗 Connected Accounts: {SessionManager.get_active_account_count()}")
    with col3:
        st.caption("☁️ Cloud Infrastructure Development Platform")

if __name__ == "__main__":
    main()