"""
Multi Cloud Intelligence Platform - Enterprise Multi-Account Cloud Infrastructure Development Platform
Multi-Account | Multi-Region | Real-Time Cloud Integration | Modern UI
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
    page_title="Multi Cloud Intelligence Platform",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply AWS Theme
AWSTheme.apply_aws_theme()

def main():
    """Main application entry point"""
    
    # Initialize session
    SessionManager.initialize()
    
    # Render header
    AWSTheme.aws_header(
        "Multi Cloud Intelligence Platform",
        "Enterprise Multi-Account Cloud Infrastructure Development Platform"
    )
    
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
        st.caption("☁️ Multi Cloud Intelligence Platform")

if __name__ == "__main__":
    main()
