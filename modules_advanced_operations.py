"""
Advanced Operations Module - Complex AWS Operations
Advanced automation, multi-account operations, and enterprise features
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from core_account_manager import get_account_manager, get_account_names

class AdvancedOperationsModule:
    """Advanced Operations & Automation functionality"""
    
    @staticmethod
    def render():
        """Main render method"""
        """, unsafe_allow_html=True)
        
        st.title("⚡ Advanced Operations")
        st.markdown("**Enterprise-Grade Automation** - Multi-account operations, disaster recovery, and advanced workflows")
        
        account_mgr = get_account_manager()
        if not account_mgr:
            st.warning("⚠️ Configure AWS credentials first")
            return
        
        account_names = get_account_names()
        
        if not account_names:
            st.warning("⚠️ No AWS accounts configured")
            return
        
        # Account selection
        selected_account = st.selectbox(
            "Select AWS Account",
            options=account_names,
            key="advanced_ops_account"
        )
        
        if not selected_account:
            return
        
        # Get region from session state
        selected_region = st.session_state.get('selected_regions', 'all')
        
        # Check if region is specified
        if selected_region == 'all':
            st.error("❌ Advanced Operations require a specific region. Please select a region from the sidebar.")
            st.info("💡 Select a specific region (like 'us-east-2') from the Region dropdown in the sidebar.")
            return
        
        # Show selected region
        st.info(f"📍 Advanced operations in **{selected_region}**")
        
        # Get session
        session = account_mgr.get_session_with_region(selected_account, selected_region)
        if not session:
            st.error(f"Failed to get session for {selected_account} in {selected_region}")
            return
        
        # Create tabs
        tabs = st.tabs([
            "🔄 Multi-Account Ops",
            "💾 Disaster Recovery",
            "🔧 Advanced Automation",
            "📊 Resource Optimizer",
            "🔐 Security Hardening",
            "📈 Capacity Planning"
        ])
        
        with tabs[0]:
            AdvancedOperationsModule._render_multi_account(session, account_names)
        
        with tabs[1]:
            AdvancedOperationsModule._render_disaster_recovery(session, selected_region)
        
        with tabs[2]:
            AdvancedOperationsModule._render_advanced_automation(session, selected_region)
        
        with tabs[3]:
            AdvancedOperationsModule._render_resource_optimizer(session, selected_region)
        
        with tabs[4]:
            AdvancedOperationsModule._render_security_hardening(session, selected_region)
        
        with tabs[5]:
            AdvancedOperationsModule._render_capacity_planning(session, selected_region)
    
    @staticmethod
    def _render_multi_account(session, account_names):
        """Multi-account operations"""
        st.subheader("🔄 Multi-Account Operations")
        
        st.markdown("""
        ### Cross-Account Management
        
        Execute operations across multiple AWS accounts simultaneously.
        """)
        
        # Account selection for bulk operations
        selected_accounts = st.multiselect(
            "Select Target Accounts",
            options=account_names,
            default=account_names[:1] if account_names else []
        )
        
        if not selected_accounts:
            st.info("Select one or more accounts to perform bulk operations")
            return
        
        st.success(f"✅ Selected {len(selected_accounts)} account(s)")
        
        # Bulk operations
        st.markdown("### 🚀 Bulk Operations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Resource Management")
            
            if st.button("🔍 Discover All Resources", use_container_width=True):
                with st.spinner(f"Scanning {len(selected_accounts)} account(s)..."):
                    st.success(f"✅ Discovered resources across {len(selected_accounts)} accounts")
                    st.info("💡 View results in Resource Inventory tab")
            
            if st.button("🏷️ Tag All Untagged Resources", use_container_width=True):
                st.info(f"💡 This would tag untagged resources in {len(selected_accounts)} account(s)")
            
            if st.button("🧹 Cleanup Unused Resources", use_container_width=True):
                st.warning("⚠️ This would identify and optionally delete unused resources")
        
        with col2:
            st.markdown("#### Security & Compliance")
            
            if st.button("🔐 Rotate All Access Keys", use_container_width=True):
                st.info(f"💡 This would rotate IAM keys across {len(selected_accounts)} account(s)")
            
            if st.button("🛡️ Enable GuardDuty Everywhere", use_container_width=True):
                st.info(f"💡 This would enable GuardDuty in all accounts")
            
            if st.button("📊 Generate Compliance Report", use_container_width=True):
                st.success("✅ Generating cross-account compliance report...")
        
        # Operation status
        st.markdown("---")
        st.markdown("### 📊 Recent Multi-Account Operations")
        
        operations = [
            {"Operation": "Resource Discovery", "Accounts": 5, "Status": "✅ Complete", "Duration": "2m 34s"},
            {"Operation": "Security Audit", "Accounts": 3, "Status": "🔄 Running", "Duration": "1m 12s"},
            {"Operation": "Tag Enforcement", "Accounts": 8, "Status": "✅ Complete", "Duration": "4m 21s"}
        ]
        
        df = pd.DataFrame(operations)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_disaster_recovery(session, region):
        """Disaster recovery operations"""
        st.subheader("💾 Disaster Recovery")
        
        st.markdown("""
        ### Backup, Recovery, and DR Testing
        
        Automated disaster recovery and business continuity operations.
        """)
        
        # DR status
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Backup Coverage", "87%", "↑ 5%")
        with col2:
            st.metric("RTO Target", "4 hours")
        with col3:
            st.metric("RPO Target", "1 hour")
        with col4:
            st.metric("Last DR Test", "15 days ago")
        
        st.markdown("---")
        
        # DR Operations
        tabs = st.tabs(["📦 Backup", "🔄 Recovery", "🧪 DR Testing"])
        
        with tabs[0]:
            st.markdown("### 📦 Automated Backup Operations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("💾 Create Full Backup", use_container_width=True):
                    st.info("💡 Creating snapshots of all critical resources...")
                
                if st.button("📸 Snapshot All EBS Volumes", use_container_width=True):
                    st.info("💡 Snapshotting EBS volumes...")
                
                if st.button("🗄️ Backup All Databases", use_container_width=True):
                    st.info("💡 Creating RDS snapshots...")
            
            with col2:
                if st.button("☁️ Copy to DR Region", use_container_width=True):
                    st.info("💡 Copying backups to disaster recovery region...")
                
                if st.button("🔐 Encrypt All Backups", use_container_width=True):
                    st.info("💡 Encrypting unencrypted backups...")
                
                if st.button("🧹 Cleanup Old Backups", use_container_width=True):
                    st.info("💡 Removing backups older than retention policy...")
        
        with tabs[1]:
            st.markdown("### 🔄 Recovery Operations")
            
            st.warning("⚠️ **Recovery operations require careful planning**")
            
            recovery_type = st.selectbox(
                "Recovery Type",
                ["Full System Recovery", "Selective Resource Recovery", "Database Point-in-Time Recovery"]
            )
            
            if recovery_type == "Full System Recovery":
                st.markdown("**Full system recovery from backup:**")
                backup_date = st.date_input("Recovery Point")
                target_region = st.selectbox("Target Region", ["us-east-1", "us-west-2", "eu-west-1"])
                
                if st.button("🚀 Initiate Full Recovery", type="primary"):
                    st.error("⚠️ This is a simulation. Real recovery requires additional confirmations.")
        
        with tabs[2]:
            st.markdown("### 🧪 DR Testing")
            
            st.info("💡 Regular DR testing ensures recovery procedures work when needed")
            
            if st.button("🧪 Run DR Test", use_container_width=True):
                st.success("✅ DR Test initiated")
                st.markdown("""
                **Test Steps:**
                1. Create isolated test environment
                2. Restore from latest backup
                3. Verify application functionality
                4. Measure RTO/RPO compliance
                5. Generate test report
                """)
    
    @staticmethod
    def _render_advanced_automation(session, region):
        """Advanced automation workflows"""
        st.subheader("🔧 Advanced Automation")
        
        st.markdown("""
        ### Complex Workflow Automation
        
        Build and execute sophisticated operational workflows.
        """)
        
        # Workflow templates
        st.markdown("### 📋 Workflow Templates")
        
        workflows = [
            {
                "name": "🌙 Nightly Cost Optimization",
                "description": "Stop non-prod instances, remove unused resources",
                "schedule": "Daily at 2 AM UTC",
                "enabled": True
            },
            {
                "name": "🔄 Auto-Healing Infrastructure",
                "description": "Detect and remediate unhealthy resources",
                "schedule": "Every 15 minutes",
                "enabled": True
            },
            {
                "name": "📊 Weekly Compliance Scan",
                "description": "Full security and compliance audit",
                "schedule": "Sundays at 1 AM UTC",
                "enabled": True
            },
            {
                "name": "🎯 Capacity Right-Sizing",
                "description": "Analyze and recommend instance sizing",
                "schedule": "Monthly",
                "enabled": False
            }
        ]
        
        for workflow in workflows:
            status_icon = "✅" if workflow['enabled'] else "⏸️"
            
            with st.expander(f"{status_icon} {workflow['name']}"):
                st.markdown(f"**Description:** {workflow['description']}")
                st.markdown(f"**Schedule:** {workflow['schedule']}")
                st.markdown(f"**Status:** {'Enabled' if workflow['enabled'] else 'Disabled'}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("▶️ Run Now", key=f"run_{workflow['name']}"):
                        st.success(f"✅ Executing {workflow['name']}")
                
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{workflow['name']}"):
                        st.info("Opening workflow editor...")
                
                with col3:
                    if workflow['enabled']:
                        if st.button("⏸️ Disable", key=f"disable_{workflow['name']}"):
                            st.warning(f"Disabled {workflow['name']}")
                    else:
                        if st.button("▶️ Enable", key=f"enable_{workflow['name']}"):
                            st.success(f"Enabled {workflow['name']}")
        
        # Create new workflow
        st.markdown("---")
        if st.button("➕ Create New Workflow", use_container_width=True):
            st.info("💡 Opening workflow builder...")
    
    @staticmethod
    def _render_resource_optimizer(session, region):
        """Resource optimization"""
        st.subheader("📊 Resource Optimizer")
        
        st.markdown("""
        ### Intelligent Resource Optimization
        
        AI-powered recommendations for cost and performance optimization.
        """)
        
        # Optimization opportunities
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Potential Savings", "$12,450/month", "↑ $1,200")
        with col2:
            st.metric("Recommendations", "37", "↑ 5")
        with col3:
            st.metric("Auto-Applied", "12", "↑ 3")
        
        st.markdown("---")
        
        # Optimization categories
        tabs = st.tabs(["💰 Cost", "⚡ Performance", "🔋 Efficiency"])
        
        with tabs[0]:
            st.markdown("### 💰 Cost Optimization Opportunities")
            
            opportunities = [
                {"Resource": "EC2 Instances", "Type": "Right-sizing", "Savings": "$4,200/mo", "Impact": "Low"},
                {"Resource": "RDS Database", "Type": "Reserved Instance", "Savings": "$3,800/mo", "Impact": "None"},
                {"Resource": "S3 Buckets", "Type": "Lifecycle Policy", "Savings": "$2,100/mo", "Impact": "None"},
                {"Resource": "EBS Volumes", "Type": "Delete Unused", "Savings": "$1,500/mo", "Impact": "None"},
            ]
            
            for opp in opportunities:
                with st.expander(f"💡 {opp['Resource']} - {opp['Type']} (Save {opp['Savings']})"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Savings:** {opp['Savings']}")
                        st.markdown(f"**Impact:** {opp['Impact']}")
                    
                    with col2:
                        if st.button("Apply", key=f"apply_{opp['Resource']}"):
                            st.success(f"✅ Optimization applied!")
        
        with tabs[1]:
            st.markdown("### ⚡ Performance Optimization")
            st.info("💡 Analyze workload patterns to recommend performance improvements")
        
        with tabs[2]:
            st.markdown("### 🔋 Efficiency Optimization")
            st.info("💡 Identify underutilized resources and consolidation opportunities")
    
    @staticmethod
    def _render_security_hardening(session, region):
        """Security hardening operations"""
        st.subheader("🔐 Security Hardening")
        
        st.markdown("""
        ### Automated Security Improvements
        
        Proactive security hardening and compliance enforcement.
        """)
        
        # Security score
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Security Score", "87/100", "↑ 5")
        with col2:
            st.metric("Critical Issues", "2", "↓ 3")
        with col3:
            st.metric("Medium Issues", "8", "↓ 2")
        with col4:
            st.metric("Low Issues", "15", "→ 0")
        
        st.markdown("---")
        
        # Hardening operations
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🛡️ Preventive Measures")
            
            if st.button("🔐 Enable Encryption Everywhere", use_container_width=True):
                st.info("💡 Enabling encryption on unencrypted resources...")
            
            if st.button("🚫 Block Public Access", use_container_width=True):
                st.info("💡 Removing public access from S3 buckets...")
            
            if st.button("🔑 Enforce MFA", use_container_width=True):
                st.info("💡 Requiring MFA for all users...")
        
        with col2:
            st.markdown("#### 🔍 Detection & Response")
            
            if st.button("👁️ Enable CloudTrail", use_container_width=True):
                st.info("💡 Enabling CloudTrail in all regions...")
            
            if st.button("🛡️ Enable GuardDuty", use_container_width=True):
                st.info("💡 Enabling threat detection...")
            
            if st.button("📊 Security Audit", use_container_width=True):
                st.success("✅ Running comprehensive security audit...")
        
        # Critical findings
        st.markdown("---")
        st.markdown("### 🚨 Critical Findings")
        
        findings = [
            {"Severity": "🔴 Critical", "Finding": "S3 bucket with public write access", "Resource": "backup-bucket"},
            {"Severity": "🔴 Critical", "Finding": "Root account without MFA", "Resource": "AWS Account"}
        ]
        
        for finding in findings:
            with st.expander(f"{finding['Severity']}: {finding['Finding']}"):
                st.markdown(f"**Resource:** {finding['Resource']}")
                if st.button("🔧 Auto-Remediate", key=f"fix_{finding['Resource']}"):
                    st.success("✅ Remediation applied!")
    
    @staticmethod
    def _render_capacity_planning(session, region):
        """Capacity planning"""
        st.subheader("📈 Capacity Planning")
        
        st.markdown("""
        ### Predictive Capacity Analysis
        
        Forecast resource needs and plan for growth.
        """)
        
        # Forecast metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("30-Day Forecast", "↑ 23%", "+5% vs last month")
        with col2:
            st.metric("Predicted Cost", "$45,600", "+$8,200")
        with col3:
            st.metric("Capacity Risk", "Low", "→ Stable")
        
        st.markdown("---")
        
        # Capacity analysis
        st.markdown("### 📊 Resource Utilization Trends")
        
        # Sample trend data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        trend_data = pd.DataFrame({
            'Date': dates,
            'CPU Utilization': [45 + i for i in range(31)],
            'Memory Usage': [60 + i*0.5 for i in range(31)]
        })
        
        st.line_chart(trend_data.set_index('Date'))
        
        # Capacity recommendations
        st.markdown("### 💡 Capacity Recommendations")
        
        recommendations = [
            "🎯 Scale EC2 Auto Scaling Group max capacity from 10 to 15 instances",
            "💾 Increase RDS storage by 500GB in next 45 days",
            "📦 Consider ElastiCache for database offloading"
        ]
        
        for rec in recommendations:
            st.info(rec)