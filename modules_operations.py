"""
Operations Module - On-Demand Operations & Automation
Instance management, automation, scaling, and operational tasks
"""

import streamlit as st
import pandas as pd
from core_account_manager import get_account_manager, get_account_names

class OperationsModule:
    """Operations & Automation functionality"""
    
    @staticmethod
    def render():
        """Main render method"""
        st.title("⚙️ Operations & Automation")
        
        account_mgr = get_account_manager()
        if not account_mgr:
            st.warning("⚠️ Configure AWS credentials first")
            st.info("👉 Go to the 'Account Management' tab to add your AWS accounts first.")
            return
        
        # Get account names
        account_names = get_account_names()
        
        if not account_names:
            st.warning("⚠️ No AWS accounts configured")
            st.info("👉 Go to the 'Account Management' tab to add your AWS accounts first.")
            return
        
        # Account selection
        selected_account = st.selectbox(
            "Select AWS Account",
            options=account_names,
            key="operations_account"
        )
        
        if not selected_account:
            return
        
        # Get region from session state
        selected_region = st.session_state.get('selected_regions', 'all')
        
        # Check if region is specified
        if selected_region == 'all':
            st.error("❌ Operations are region-specific. Please select a region from the sidebar.")
            st.info("💡 Select a specific region (like 'us-east-2') from the Region dropdown in the sidebar.")
            return
        
        # Show selected region
        st.info(f"📍 Managing operations in **{selected_region}**")
        
        # Get region-specific session
        session = account_mgr.get_session_with_region(selected_account, selected_region)
        if not session:
            st.error(f"Failed to get session for {selected_account} in region {selected_region}")
            return
        
        # Create tabs
        tabs = st.tabs([
            "💻 Instance Operations",
            "🔄 Automation",
            "📊 Scaling",
            "🔧 Maintenance",
            "📦 System Manager"
        ])
        
        with tabs[0]:
            OperationsModule._render_instance_ops(session, selected_region)
        
        with tabs[1]:
            OperationsModule._render_automation(session, selected_region)
        
        with tabs[2]:
            OperationsModule._render_scaling(session, selected_region)
        
        with tabs[3]:
            OperationsModule._render_maintenance()
        
        with tabs[4]:
            OperationsModule._render_system_manager(session)
    
    @staticmethod
    def _render_instance_ops(session, region):
        """Instance operations with direct boto3 calls"""
        st.subheader("💻 Instance Operations")
        
        try:
            # Direct EC2 client call
            ec2 = session.client('ec2')
            
            # Get instances
            response = ec2.describe_instances()
            
            # Parse instances
            instances = []
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    # Get instance name from tags
                    name = "Unnamed"
                    for tag in instance.get('Tags', []):
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                            break
                    
                    instances.append({
                        'instance_id': instance['InstanceId'],
                        'name': name,
                        'state': instance['State']['Name'],
                        'instance_type': instance['InstanceType'],
                        'availability_zone': instance['Placement']['AvailabilityZone'],
                        'private_ip': instance.get('PrivateIpAddress', 'N/A'),
                        'public_ip': instance.get('PublicIpAddress', 'N/A'),
                        'launch_time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
                    })
            
            if not instances:
                st.info(f"🔍 No EC2 instances found in {region}")
                st.markdown("""
                **To see instances here:**
                - Launch EC2 instances in this region using the Provisioning tab
                - Or select a different region with existing instances
                """)
                return
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            running = sum(1 for i in instances if i['state'] == 'running')
            stopped = sum(1 for i in instances if i['state'] == 'stopped')
            
            with col1:
                st.metric("Total Instances", len(instances))
            with col2:
                st.metric("🟢 Running", running)
            with col3:
                st.metric("🔴 Stopped", stopped)
            with col4:
                st.metric("🟡 Other", len(instances) - running - stopped)
            
            # Instance list
            st.markdown("### 📋 Instance List")
            
            for instance in instances:
                state = instance['state']
                status_icon = {
                    'running': '🟢',
                    'stopped': '🔴',
                    'pending': '🟡',
                    'stopping': '🟡',
                    'shutting-down': '🟡',
                    'terminated': '⚫'
                }.get(state, '⚪')
                
                with st.expander(f"{status_icon} {instance['name']} - {instance['instance_id']} ({state})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown(f"**Instance ID:** `{instance['instance_id']}`")
                        st.markdown(f"**Type:** `{instance['instance_type']}`")
                        st.markdown(f"**State:** `{instance['state']}`")
                    
                    with col2:
                        st.markdown(f"**AZ:** `{instance['availability_zone']}`")
                        st.markdown(f"**Private IP:** `{instance['private_ip']}`")
                        st.markdown(f"**Public IP:** `{instance['public_ip']}`")
                    
                    with col3:
                        st.markdown(f"**Launch Time:** `{instance['launch_time']}`")
                    
                    # Quick actions
                    st.markdown("**Quick Actions:**")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if state == 'stopped':
                            if st.button("▶️ Start", key=f"start_{instance['instance_id']}"):
                                try:
                                    ec2.start_instances(InstanceIds=[instance['instance_id']])
                                    st.success(f"✅ Starting {instance['name']}")
                                except Exception as e:
                                    st.error(f"Failed: {str(e)}")
                        elif state == 'running':
                            if st.button("⏸️ Stop", key=f"stop_{instance['instance_id']}"):
                                try:
                                    ec2.stop_instances(InstanceIds=[instance['instance_id']])
                                    st.warning(f"⏸️ Stopping {instance['name']}")
                                except Exception as e:
                                    st.error(f"Failed: {str(e)}")
                    
                    with col2:
                        if state == 'running':
                            if st.button("🔄 Reboot", key=f"reboot_{instance['instance_id']}"):
                                try:
                                    ec2.reboot_instances(InstanceIds=[instance['instance_id']])
                                    st.info(f"🔄 Rebooting {instance['name']}")
                                except Exception as e:
                                    st.error(f"Failed: {str(e)}")
                    
                    with col3:
                        if st.button("📊 Details", key=f"details_{instance['instance_id']}"):
                            st.json(instance)
                    
                    with col4:
                        if st.button("🔗 Console", key=f"console_{instance['instance_id']}"):
                            console_url = f"https://{region}.console.aws.amazon.com/ec2/v2/home?region={region}#Instances:instanceId={instance['instance_id']}"
                            st.markdown(f"[Open in Console]({console_url})")
        
        except Exception as e:
            st.error(f"❌ Error loading instances: {str(e)}")
            
            if "AccessDenied" in str(e):
                st.info("""
                **IAM Permissions Required:**
                - ec2:DescribeInstances
                - ec2:StartInstances
                - ec2:StopInstances
                - ec2:RebootInstances
                
                Add these to your CloudIDP-Access role.
                """)
            else:
                st.info("💡 Make sure you have EC2 permissions and instances in this region")
    
    @staticmethod
    def _render_automation(session, region):
        """Automation workflows"""
        st.subheader("🔄 Automation Workflows")
        
        st.markdown("""
        ### Quick Automation Tasks
        
        Common operational automation tasks for your AWS infrastructure.
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔄 Instance Operations")
            
            if st.button("🔄 Restart All Web Servers", use_container_width=True):
                st.info("💡 This would restart instances tagged as 'web-server'")
            
            if st.button("⏸️ Stop Dev Instances", use_container_width=True):
                st.info("💡 This would stop instances tagged as 'environment: dev'")
            
            if st.button("💾 Create AMI Snapshots", use_container_width=True):
                st.info("💡 This would create AMIs of all production instances")
        
        with col2:
            st.markdown("#### 📦 Maintenance")
            
            if st.button("📦 Update All Packages", use_container_width=True):
                st.info("💡 This would run yum/apt update on all instances")
            
            if st.button("🧹 Cleanup Old Snapshots", use_container_width=True):
                st.info("💡 This would delete snapshots older than 30 days")
            
            if st.button("🔐 Rotate Access Keys", use_container_width=True):
                st.info("💡 This would rotate IAM access keys")
        
        st.markdown("---")
        st.info("💡 **Automation Note:** These are placeholder actions. Connect to AWS Systems Manager to enable automated workflows.")
    
    @staticmethod
    def _render_scaling(session, region):
        """Scaling operations"""
        st.subheader("📊 Auto Scaling")
        
        try:
            autoscaling = session.client('autoscaling')
            
            # Get Auto Scaling Groups
            response = autoscaling.describe_auto_scaling_groups()
            asgs = response.get('AutoScalingGroups', [])
            
            if not asgs:
                st.info("🔍 No Auto Scaling Groups found in this region")
                st.markdown("""
                **To see Auto Scaling Groups:**
                - Create ASGs using the Provisioning tab
                - Or select a different region
                """)
                return
            
            st.metric("Total ASGs", len(asgs))
            
            for asg in asgs:
                name = asg['AutoScalingGroupName']
                desired = asg['DesiredCapacity']
                min_size = asg['MinSize']
                max_size = asg['MaxSize']
                current = len(asg['Instances'])
                
                with st.expander(f"📊 {name}"):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Desired", desired)
                    with col2:
                        st.metric("Current", current)
                    with col3:
                        st.metric("Min", min_size)
                    with col4:
                        st.metric("Max", max_size)
                    
                    # Scaling actions
                    new_desired = st.slider(
                        "Set Desired Capacity",
                        min_value=min_size,
                        max_value=max_size,
                        value=desired,
                        key=f"scale_{name}"
                    )
                    
                    if st.button(f"Apply New Capacity: {new_desired}", key=f"apply_{name}"):
                        try:
                            autoscaling.set_desired_capacity(
                                AutoScalingGroupName=name,
                                DesiredCapacity=new_desired
                            )
                            st.success(f"✅ Scaling {name} to {new_desired} instances")
                        except Exception as e:
                            st.error(f"Failed: {str(e)}")
        
        except Exception as e:
            st.error(f"Error loading Auto Scaling Groups: {str(e)}")
            st.info("💡 Make sure you have autoscaling:Describe* permissions")
    
    @staticmethod
    def _render_maintenance():
        """Maintenance windows"""
        st.subheader("🔧 Maintenance Windows")
        
        st.markdown("""
        ### Schedule Maintenance Tasks
        
        Define maintenance windows for automated tasks and updates.
        """)
        
        # Sample maintenance windows
        maintenance_windows = [
            {
                "name": "Weekly Patching",
                "schedule": "Every Sunday 2:00 AM UTC",
                "duration": "4 hours",
                "enabled": True,
                "next_run": "2025-12-08 02:00 UTC"
            },
            {
                "name": "Monthly AMI Creation",
                "schedule": "First Sunday 1:00 AM UTC",
                "duration": "2 hours",
                "enabled": True,
                "next_run": "2026-01-05 01:00 UTC"
            },
            {
                "name": "Quarterly DR Test",
                "schedule": "First Saturday of Quarter",
                "duration": "8 hours",
                "enabled": False,
                "next_run": "Not scheduled"
            }
        ]
        
        for mw in maintenance_windows:
            status_icon = "✅" if mw['enabled'] else "⏸️"
            
            with st.expander(f"{status_icon} {mw['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Schedule:** {mw['schedule']}")
                    st.markdown(f"**Duration:** {mw['duration']}")
                    st.markdown(f"**Next Run:** {mw['next_run']}")
                
                with col2:
                    st.markdown(f"**Status:** {'✅ Enabled' if mw['enabled'] else '⏸️ Disabled'}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", key=f"edit_{mw['name']}"):
                        st.info(f"Editing {mw['name']} configuration")
                
                with col2:
                    if mw['enabled']:
                        if st.button("⏸️ Disable", key=f"disable_{mw['name']}"):
                            st.warning(f"Disabled {mw['name']}")
                    else:
                        if st.button("▶️ Enable", key=f"enable_{mw['name']}"):
                            st.success(f"Enabled {mw['name']}")
    
    @staticmethod
    def _render_system_manager(session):
        """Systems Manager integration"""
        st.subheader("📦 AWS Systems Manager")
        
        st.markdown("""
        ### Systems Manager Features
        
        Manage and monitor your infrastructure with AWS Systems Manager.
        """)
        
        tabs = st.tabs([
            "📊 Inventory",
            "📦 Patch Manager",
            "🔧 Session Manager",
            "📝 Run Command"
        ])
        
        with tabs[0]:
            st.markdown("#### 📊 Managed Instances")
            st.info("💡 Install SSM Agent on your instances to see them here")
        
        with tabs[1]:
            st.markdown("#### 📦 Patch Baselines")
            st.info("💡 Configure patch baselines to automate OS patching")
        
        with tabs[2]:
            st.markdown("#### 🔧 Connect to Instances")
            st.info("💡 Use Session Manager for secure shell access without SSH keys")
        
        with tabs[3]:
            st.markdown("#### 📝 Execute Commands")
            st.info("💡 Run commands across multiple instances simultaneously")
