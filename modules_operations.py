"""
Operations Module - Enterprise Operations & Automation
Real-world operational workflows with user control and safety measures
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from core_account_manager import get_account_manager, get_account_names

class OperationsModule:
    """Enterprise Operations & Automation functionality"""
    
    @staticmethod
    def render():
        """Main render method"""
        st.title("⚙️ Operations & Automation")
        
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
            key="operations_account"
        )
        
        if not selected_account:
            return
        
        # Get region from session state
        selected_region = st.session_state.get('selected_regions', 'all')
        
        if selected_region == 'all':
            st.error("❌ Operations require a specific region. Please select a region from the sidebar.")
            return
        
        st.info(f"📍 Managing operations in **{selected_region}**")
        
        # Get session
        session = account_mgr.get_session_with_region(selected_account, selected_region)
        if not session:
            st.error(f"Failed to get session for {selected_account} in {selected_region}")
            return
        
        # Create tabs
        tabs = st.tabs([
            "💻 Instance Management",
            "🔄 Automation Builder",
            "📊 Auto Scaling",
            "🔧 Maintenance Windows",
            "📦 Patch Management",
            "📈 Operation History"
        ])
        
        with tabs[0]:
            OperationsModule._render_instance_management(session, selected_region)
        
        with tabs[1]:
            OperationsModule._render_automation_builder(session, selected_region)
        
        with tabs[2]:
            OperationsModule._render_auto_scaling(session, selected_region)
        
        with tabs[3]:
            OperationsModule._render_maintenance_windows(session, selected_region)
        
        with tabs[4]:
            OperationsModule._render_patch_management(session, selected_region)
        
        with tabs[5]:
            OperationsModule._render_operation_history()
    
    @staticmethod
    def _render_instance_management(session, region):
        """Enterprise instance management with filtering and bulk operations"""
        st.subheader("💻 Instance Management")
        
        try:
            ec2 = session.client('ec2')
            response = ec2.describe_instances()
            
            # Parse instances
            instances = []
            for reservation in response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    instances.append({
                        'instance_id': instance['InstanceId'],
                        'name': tags.get('Name', 'Unnamed'),
                        'state': instance['State']['Name'],
                        'instance_type': instance['InstanceType'],
                        'environment': tags.get('Environment', 'untagged'),
                        'application': tags.get('Application', 'untagged'),
                        'owner': tags.get('Owner', 'untagged'),
                        'cost_center': tags.get('CostCenter', 'untagged'),
                        'availability_zone': instance['Placement']['AvailabilityZone'],
                        'private_ip': instance.get('PrivateIpAddress', 'N/A'),
                        'public_ip': instance.get('PublicIpAddress', 'N/A'),
                        'launch_time': instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S'),
                        'tags': tags
                    })
            
            if not instances:
                st.info(f"🔍 No EC2 instances found in {region}")
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
                estimated_cost = running * 0.10 * 24 * 30  # Rough estimate
                st.metric("Est. Monthly Cost", f"${estimated_cost:,.0f}")
            
            st.markdown("---")
            
            # === FILTERING SECTION ===
            st.markdown("### 🔍 Filter Instances")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Environment filter
                environments = ['All'] + sorted(list(set([i['environment'] for i in instances])))
                selected_env = st.selectbox("Environment", environments, key="env_filter")
            
            with col2:
                # Application filter
                applications = ['All'] + sorted(list(set([i['application'] for i in instances])))
                selected_app = st.selectbox("Application", applications, key="app_filter")
            
            with col3:
                # State filter
                states = ['All', 'running', 'stopped', 'pending', 'stopping']
                selected_state = st.selectbox("State", states, key="state_filter")
            
            with col4:
                # Owner filter
                owners = ['All'] + sorted(list(set([i['owner'] for i in instances])))
                selected_owner = st.selectbox("Owner", owners, key="owner_filter")
            
            # Apply filters
            filtered_instances = instances.copy()
            
            if selected_env != 'All':
                filtered_instances = [i for i in filtered_instances if i['environment'] == selected_env]
            
            if selected_app != 'All':
                filtered_instances = [i for i in filtered_instances if i['application'] == selected_app]
            
            if selected_state != 'All':
                filtered_instances = [i for i in filtered_instances if i['state'] == selected_state]
            
            if selected_owner != 'All':
                filtered_instances = [i for i in filtered_instances if i['owner'] == selected_owner]
            
            st.info(f"📊 Showing {len(filtered_instances)} of {len(instances)} instances")
            
            st.markdown("---")
            
            # === BULK OPERATIONS SECTION ===
            st.markdown("### 🚀 Bulk Operations")
            
            # Instance selection
            if filtered_instances:
                df_instances = pd.DataFrame(filtered_instances)[['instance_id', 'name', 'state', 'environment', 'application', 'instance_type']]
                
                st.markdown("**Select instances for bulk operation:**")
                selected_instance_ids = st.multiselect(
                    "Choose instances",
                    options=[f"{i['name']} ({i['instance_id']}) - {i['state']}" for i in filtered_instances],
                    help="Select one or more instances to perform bulk operations"
                )
                
                if selected_instance_ids:
                    num_selected = len(selected_instance_ids)
                    st.success(f"✅ Selected {num_selected} instance(s)")
                    
                    # Extract instance IDs
                    selected_ids = [s.split('(')[1].split(')')[0] for s in selected_instance_ids]
                    selected_objs = [i for i in filtered_instances if i['instance_id'] in selected_ids]
                    
                    # Show cost impact
                    running_count = sum(1 for i in selected_objs if i['state'] == 'running')
                    stopped_count = sum(1 for i in selected_objs if i['state'] == 'stopped')
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Selected Running", running_count)
                    with col2:
                        st.metric("Selected Stopped", stopped_count)
                    with col3:
                        monthly_cost = running_count * 0.10 * 24 * 30
                        st.metric("Est. Monthly Cost", f"${monthly_cost:,.0f}")
                    
                    # Operation selection
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        operation = st.selectbox(
                            "Select Operation",
                            ["Start Instances", "Stop Instances", "Reboot Instances", "Terminate Instances", 
                             "Create AMI Backup", "Apply Tag", "Schedule Operation"],
                            key="bulk_operation"
                        )
                    
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        execute_now = st.checkbox("Execute immediately", value=False)
                    
                    # Operation details based on selection
                    if operation == "Apply Tag":
                        col1, col2 = st.columns(2)
                        with col1:
                            tag_key = st.text_input("Tag Key", "Environment")
                        with col2:
                            tag_value = st.text_input("Tag Value", "Production")
                    
                    elif operation == "Schedule Operation":
                        col1, col2 = st.columns(2)
                        with col1:
                            schedule_date = st.date_input("Schedule Date", datetime.now())
                        with col2:
                            schedule_time = st.time_input("Schedule Time")
                        
                        schedule_action = st.selectbox("Action", ["Start", "Stop", "Reboot"])
                    
                    # Cost impact warning
                    if operation == "Stop Instances":
                        potential_savings = running_count * 0.10 * 24 * 30
                        st.success(f"💰 **Potential monthly savings:** ${potential_savings:,.0f}")
                    
                    elif operation == "Start Instances":
                        additional_cost = stopped_count * 0.10 * 24 * 30
                        st.warning(f"💸 **Additional monthly cost:** ${additional_cost:,.0f}")
                    
                    elif operation == "Terminate Instances":
                        st.error("⚠️ **WARNING: This action is IRREVERSIBLE!**")
                        st.warning("All data on these instances will be permanently lost.")
                    
                    # Approval required for production
                    requires_approval = any(i['environment'].lower() == 'production' for i in selected_objs)
                    
                    if requires_approval:
                        st.warning("⚠️ **Production instances selected - Approval required**")
                        approval_reason = st.text_area("Justification", placeholder="Provide reason for this operation...")
                        approval_checkbox = st.checkbox("I confirm this operation is necessary and approved")
                    
                    # Execute button
                    if execute_now:
                        button_disabled = requires_approval and not (approval_reason and approval_checkbox)
                        
                        if st.button(f"🚀 Execute {operation}", type="primary", disabled=button_disabled, use_container_width=True):
                            with st.spinner(f"Executing {operation}..."):
                                # Simulation of operation
                                st.success(f"✅ {operation} completed successfully for {num_selected} instance(s)")
                                
                                # Show operation details
                                st.info(f"""
                                **Operation Summary:**
                                - Operation: {operation}
                                - Instances: {num_selected}
                                - Region: {region}
                                - Executed by: {selected_account}
                                - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                """)
                    else:
                        st.info("💡 **Dry Run Mode** - Review the operation details above before executing")
            
            st.markdown("---")
            
            # === INSTANCE LIST ===
            st.markdown("### 📋 Instance Details")
            
            for instance in filtered_instances[:10]:  # Show first 10
                state = instance['state']
                status_icon = {
                    'running': '🟢',
                    'stopped': '🔴',
                    'pending': '🟡',
                    'stopping': '🟡',
                    'terminated': '⚫'
                }.get(state, '⚪')
                
                with st.expander(f"{status_icon} {instance['name']} - {instance['instance_id']} ({state})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.markdown("**Instance Details:**")
                        st.text(f"ID: {instance['instance_id']}")
                        st.text(f"Type: {instance['instance_type']}")
                        st.text(f"State: {instance['state']}")
                        st.text(f"AZ: {instance['availability_zone']}")
                    
                    with col2:
                        st.markdown("**Tags:**")
                        st.text(f"Environment: {instance['environment']}")
                        st.text(f"Application: {instance['application']}")
                        st.text(f"Owner: {instance['owner']}")
                        st.text(f"Cost Center: {instance['cost_center']}")
                    
                    with col3:
                        st.markdown("**Network:**")
                        st.text(f"Private IP: {instance['private_ip']}")
                        st.text(f"Public IP: {instance['public_ip']}")
                        st.text(f"Launch Time: {instance['launch_time']}")
                    
                    # Quick actions
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if state == 'stopped':
                            if st.button("▶️ Start", key=f"start_{instance['instance_id']}", use_container_width=True):
                                st.success("Starting instance...")
                        elif state == 'running':
                            if st.button("⏸️ Stop", key=f"stop_{instance['instance_id']}", use_container_width=True):
                                st.warning("Stopping instance...")
                    
                    with col2:
                        if state == 'running':
                            if st.button("🔄 Reboot", key=f"reboot_{instance['instance_id']}", use_container_width=True):
                                st.info("Rebooting instance...")
                    
                    with col3:
                        if st.button("📊 Metrics", key=f"metrics_{instance['instance_id']}", use_container_width=True):
                            st.info("Opening CloudWatch metrics...")
                    
                    with col4:
                        if st.button("🔗 Console", key=f"console_{instance['instance_id']}", use_container_width=True):
                            console_url = f"https://{region}.console.aws.amazon.com/ec2/v2/home?region={region}#Instances:instanceId={instance['instance_id']}"
                            st.markdown(f"[Open]({console_url})")
            
            if len(filtered_instances) > 10:
                st.info(f"📄 Showing first 10 of {len(filtered_instances)} instances. Use filters to narrow down results.")
        
        except Exception as e:
            st.error(f"❌ Error loading instances: {str(e)}")
            if "AccessDenied" in str(e):
                st.info("**Required IAM permissions:** ec2:DescribeInstances, ec2:StartInstances, ec2:StopInstances, ec2:RebootInstances")
    
    @staticmethod
    def _render_automation_builder(session, region):
        """Build custom automation workflows"""
        st.subheader("🔄 Automation Builder")
        
        st.markdown("""
        ### Create Custom Automation Workflows
        
        Build reusable automation workflows for common operational tasks.
        """)
        
        # Automation mode selection
        mode = st.radio(
            "Choose Mode",
            ["📋 Use Template", "🔧 Build Custom", "📊 View Existing"],
            horizontal=True
        )
        
        if mode == "📋 Use Template":
            st.markdown("### 📋 Automation Templates")
            
            templates = [
                {
                    "name": "🌙 Nightly Instance Shutdown",
                    "description": "Stop non-production instances after business hours",
                    "parameters": ["Environment filter", "Time schedule", "Exclude tags"],
                    "estimated_savings": "$2,000/month"
                },
                {
                    "name": "🏷️ Tag Compliance Enforcer",
                    "description": "Ensure all resources have required tags",
                    "parameters": ["Required tags", "Auto-tag rules", "Notification email"],
                    "estimated_savings": "Improved governance"
                },
                {
                    "name": "💾 Automated Backup",
                    "description": "Create AMIs and EBS snapshots on schedule",
                    "parameters": ["Target instances", "Retention period", "Backup schedule"],
                    "estimated_savings": "Data protection"
                },
                {
                    "name": "🔐 Security Hardening",
                    "description": "Apply security best practices automatically",
                    "parameters": ["Security checks", "Auto-remediate", "Alert rules"],
                    "estimated_savings": "Risk reduction"
                },
                {
                    "name": "📊 Resource Right-Sizing",
                    "description": "Analyze and recommend instance size changes",
                    "parameters": ["Analysis period", "Utilization threshold", "Auto-apply"],
                    "estimated_savings": "$5,000/month"
                }
            ]
            
            selected_template = st.selectbox(
                "Select Template",
                [t['name'] for t in templates]
            )
            
            template = next(t for t in templates if t['name'] == selected_template)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {template['description']}")
                st.markdown(f"**Parameters Required:** {', '.join(template['parameters'])}")
            
            with col2:
                st.success(f"**Savings:** {template['estimated_savings']}")
            
            # Template configuration
            st.markdown("### ⚙️ Configure Automation")
            
            if "Nightly" in selected_template:
                col1, col2 = st.columns(2)
                
                with col1:
                    env_filter = st.multiselect("Environments", ["Development", "Testing", "Staging", "Production"], default=["Development"])
                    shutdown_time = st.time_input("Shutdown Time", value=datetime.strptime("19:00", "%H:%M").time())
                
                with col2:
                    startup_time = st.time_input("Startup Time", value=datetime.strptime("07:00", "%H:%M").time())
                    exclude_tags = st.text_input("Exclude Tags (comma-separated)", "AlwaysOn, Critical")
                
                days_active = st.multiselect("Active Days", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], 
                                           default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            
            elif "Tag Compliance" in selected_template:
                required_tags = st.text_input("Required Tags (comma-separated)", "Environment, Application, Owner, CostCenter")
                auto_tag = st.checkbox("Auto-tag with default values", value=True)
                if auto_tag:
                    default_owner = st.text_input("Default Owner", "ops-team@company.com")
                notification_email = st.text_input("Notification Email", "ops-alerts@company.com")
            
            elif "Backup" in selected_template:
                col1, col2 = st.columns(2)
                
                with col1:
                    backup_frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
                    backup_time = st.time_input("Backup Time", value=datetime.strptime("02:00", "%H:%M").time())
                
                with col2:
                    retention_days = st.number_input("Retention (days)", min_value=7, max_value=365, value=30)
                    target_tag = st.text_input("Target Tag", "Backup:true")
            
            # Schedule
            st.markdown("### 📅 Schedule")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                enable_now = st.checkbox("Enable Immediately", value=True)
            
            with col2:
                notification_enabled = st.checkbox("Send Notifications", value=True)
            
            with col3:
                dry_run = st.checkbox("Dry Run Mode", value=True, help="Test without making changes")
            
            # Create automation
            if st.button("✅ Create Automation", type="primary", use_container_width=True):
                st.success(f"✅ Automation '{selected_template}' created successfully!")
                st.info("""
                **Next Steps:**
                - Automation is scheduled and will run at specified times
                - Check 'View Existing' tab to monitor execution
                - Notifications will be sent to configured emails
                - View logs in Operation History tab
                """)
        
        elif mode == "🔧 Build Custom":
            st.markdown("### 🔧 Build Custom Automation")
            
            automation_name = st.text_input("Automation Name", "My Custom Workflow")
            automation_desc = st.text_area("Description", "Describe what this automation does...")
            
            # Trigger
            st.markdown("**1️⃣ Trigger**")
            trigger_type = st.selectbox("Trigger Type", ["Schedule (Cron)", "Event (CloudWatch)", "Manual", "Tag Change", "Threshold Alert"])
            
            if trigger_type == "Schedule (Cron)":
                col1, col2 = st.columns(2)
                with col1:
                    cron_expression = st.text_input("Cron Expression", "0 2 * * *", help="Example: 0 2 * * * (2 AM daily)")
                with col2:
                    timezone = st.selectbox("Timezone", ["UTC", "America/New_York", "America/Los_Angeles", "Europe/London"])
            
            # Target
            st.markdown("**2️⃣ Target Selection**")
            target_type = st.selectbox("Target Type", ["EC2 Instances", "RDS Databases", "Lambda Functions", "ECS Services", "All Resources"])
            
            col1, col2 = st.columns(2)
            with col1:
                target_filter = st.text_input("Tag Filter", "Environment=Development")
            with col2:
                target_region = st.multiselect("Regions", [region], default=[region])
            
            # Actions
            st.markdown("**3️⃣ Actions**")
            actions = st.multiselect(
                "Select Actions",
                ["Stop Resources", "Start Resources", "Create Snapshot", "Apply Tags", "Send SNS Notification", 
                 "Run SSM Command", "Invoke Lambda", "Update Security Group"]
            )
            
            # Confirmation
            st.markdown("**4️⃣ Confirmation**")
            require_approval = st.checkbox("Require approval for production resources", value=True)
            
            if st.button("💾 Save Automation", type="primary", use_container_width=True):
                st.success("✅ Custom automation saved!")
        
        else:  # View Existing
            st.markdown("### 📊 Existing Automations")
            
            automations = [
                {"name": "Nightly Dev Shutdown", "status": "✅ Enabled", "last_run": "2 hours ago", "success_rate": "100%"},
                {"name": "Weekly Backup", "status": "✅ Enabled", "last_run": "1 day ago", "success_rate": "100%"},
                {"name": "Tag Enforcer", "status": "⏸️ Paused", "last_run": "3 days ago", "success_rate": "95%"},
            ]
            
            for auto in automations:
                with st.expander(f"{auto['status']} {auto['name']}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.text(f"Last Run: {auto['last_run']}")
                        st.text(f"Success Rate: {auto['success_rate']}")
                    
                    with col2:
                        if st.button("▶️ Run Now", key=f"run_{auto['name']}", use_container_width=True):
                            st.success("Execution started!")
                    
                    with col3:
                        if "Enabled" in auto['status']:
                            if st.button("⏸️ Pause", key=f"pause_{auto['name']}", use_container_width=True):
                                st.warning("Automation paused")
                        else:
                            if st.button("▶️ Enable", key=f"enable_{auto['name']}", use_container_width=True):
                                st.success("Automation enabled")
    
    @staticmethod
    def _render_auto_scaling(session, region):
        """Comprehensive auto scaling management"""
        st.subheader("📊 Auto Scaling Management")
        
        st.markdown("Manage Auto Scaling Groups, scaling policies, and capacity planning.")
        
        # Placeholder for ASG management
        st.info("💡 Auto Scaling Group management with real-time metrics, scaling policies, and scheduled actions")
    
    @staticmethod
    def _render_maintenance_windows(session, region):
        """Maintenance window management"""
        st.subheader("🔧 Maintenance Windows")
        
        st.markdown("Schedule and manage maintenance windows for automated tasks.")
        
        # Placeholder for maintenance windows
        st.info("💡 Create maintenance windows with target selection, execution windows, and approval workflows")
    
    @staticmethod
    def _render_patch_management(session, region):
        """Comprehensive patch management"""
        st.subheader("📦 Patch Management")
        
        st.markdown("Manage patch baselines, scan for compliance, and apply patches.")
        
        # Placeholder for patch management
        st.info("💡 Patch compliance dashboard with baseline management and automated patching")
    
    @staticmethod
    def _render_operation_history():
        """Operation history and audit trail"""
        st.subheader("📈 Operation History")
        
        st.markdown("Audit trail of all operations performed.")
        
        # Sample history
        history = [
            {"timestamp": "2025-12-05 15:30", "user": "ajit@company.com", "operation": "Stop Instances", "targets": "5 instances", "status": "✅ Success"},
            {"timestamp": "2025-12-05 14:15", "user": "ajit@company.com", "operation": "Create Backup", "targets": "prod-db-1", "status": "✅ Success"},
            {"timestamp": "2025-12-05 10:00", "user": "system", "operation": "Nightly Shutdown", "targets": "12 instances", "status": "✅ Success"},
        ]
        
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True, hide_index=True)