"""
Unified CI/CD Module - All Phases Combined
Combines Pipeline Builder, Triggering, and Approvals into one module
"""

import streamlit as st
import boto3
from core_account_manager import get_account_manager, get_account_names

class UnifiedCICDModule:
    """Unified CI/CD Module with all phases"""
    
    @staticmethod
    def render():
        """Main render method"""
        st.title("🔄 CI/CD Pipeline Management")
        st.markdown("**Complete CI/CD Platform** - Build, Trigger, and Approve Pipelines")
        
        # Get account manager
        account_mgr = get_account_manager()
        
        if not account_mgr:
            st.warning("⚠️ Please configure AWS credentials in Account Management")
            return
        
        # Get account names
        account_names = get_account_names()
        
        if not account_names:
            st.warning("⚠️ No AWS accounts configured")
            return
        
        # Account selector
        selected_account = st.selectbox(
            "Select AWS Account",
            options=account_names,
            key="unified_cicd_account_selector"
        )
        
        if not selected_account:
            st.info("Please select an account")
            return
        
        # Get region
        selected_region = st.session_state.get('selected_regions', 'us-east-1')
        if selected_region == 'all':
            selected_region = 'us-east-1'
        
        # Get session for selected account
        try:
            session = account_mgr.get_session(selected_account)
            
            # Get account ID
            sts = session.client('sts')
            account_id = sts.get_caller_identity()['Account']
            
        except Exception as e:
            st.error(f"Error getting AWS session: {str(e)}")
            return
        
        # Main phase tabs
        phase_tabs = st.tabs([
            "🏗️ Pipeline Builder",
            "⚡ Triggering & Parameters", 
            "⚠️ Approvals & Notifications"
        ])
        
        # Phase 1: Pipeline Builder
        with phase_tabs[0]:
            try:
                from modules_cicd_orchestration import CICDOrchestrationUI
                CICDOrchestrationUI.render()
            except Exception as e:
                st.error(f"Error loading Pipeline Builder: {str(e)}")
        
        # Phase 2: Triggering & Parameters
        with phase_tabs[1]:
            try:
                from modules_cicd_phase2_triggering import render_cicd_phase2_module
                render_cicd_phase2_module(session, account_id, selected_region)
            except Exception as e:
                st.error(f"Error loading Triggering module: {str(e)}")
                st.info("💡 Make sure modules_cicd_phase2_triggering.py is in your src folder")
        
        # Phase 3: Approvals & Notifications  
        with phase_tabs[2]:
            try:
                from modules_cicd_phase3_approvals import render_cicd_phase3_module
                render_cicd_phase3_module(session, account_id, selected_region)
            except Exception as e:
                st.error(f"Error loading Approvals module: {str(e)}")
                st.info("💡 Make sure modules_cicd_phase3_approvals.py is in your src folder")


# For backward compatibility
def render_unified_cicd():
    """Render function for navigation"""
    UnifiedCICDModule.render()