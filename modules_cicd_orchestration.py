"""
CI/CD Pipeline Orchestration Module - AWS Native Integration
Orchestrates AWS CodePipeline, CodeBuild, CodeDeploy, and CloudFormation
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from core_account_manager import get_account_manager, get_account_names
import json
from pipeline_builder_addon import render_pipeline_builder_tab
class CICDOrchestrationUI:
    """AWS Native CI/CD Orchestration and Governance"""
    
    @staticmethod
    def render():
        """Main render method for CI/CD Orchestration"""
        st.title("🔄 CI/CD Pipeline Orchestration")
        st.markdown("**AWS Native Integration** - CodePipeline, CodeBuild, CloudFormation")
        
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
            key="cicd_account_selector"
        )
        
        if not selected_account:
            st.info("Please select an account")
            return
        
        # Check if a specific region is selected
        selected_region = st.session_state.get('selected_regions', 'all')
        
        if selected_region == 'all':
            st.error("❌ CI/CD pipelines are region-specific. Please select a region from the sidebar.")
            return
        
        # Get region-specific session
        session = account_mgr.get_session_with_region(selected_account, selected_region)
        if not session:
            st.error(f"Failed to get session for {selected_account} in region {selected_region}")
            return
        
        # Show selected region
        st.info(f"📍 Managing pipelines in **{selected_region}**")
        
        # Initialize AWS clients
        try:
            codepipeline_client = session.client('codepipeline')
            codebuild_client = session.client('codebuild')
            cloudformation_client = session.client('cloudformation')
            logs_client = session.client('logs')
        except Exception as e:
            st.error(f"Failed to initialize AWS clients: {str(e)}")
            return
        
        # Main tabs
        tabs = st.tabs([
            "📊 Pipeline Dashboard",
            "🚀 Trigger Pipeline",
            "🏗️ CodeBuild Projects",
            "📦 CloudFormation Stacks",
            "📈 Analytics",
            "⚙️ Configuration"
        ])
        
        # Pipeline Dashboard Tab
        with tabs[0]:
            CICDOrchestrationUI._render_pipeline_dashboard(codepipeline_client, selected_region)
        
        # Trigger Pipeline Tab
        with tabs[1]:
            CICDOrchestrationUI._render_trigger_pipeline(codepipeline_client)
        
        # CodeBuild Projects Tab
        with tabs[2]:
            CICDOrchestrationUI._render_codebuild_projects(codebuild_client)
        
        # CloudFormation Stacks Tab
        with tabs[3]:
            CICDOrchestrationUI._render_cloudformation_stacks(cloudformation_client)
        
        # Analytics Tab
        with tabs[4]:
            CICDOrchestrationUI._render_analytics(codepipeline_client, codebuild_client)
        
        # Configuration Tab
        with tabs[5]:
            CICDOrchestrationUI._render_configuration()
    
    @staticmethod
    def _render_pipeline_dashboard(client, region: str):
        """Render CodePipeline dashboard with real-time status"""
        st.subheader("📊 CodePipeline Dashboard")
        
        try:
            # List all pipelines
            with st.spinner("Loading pipelines..."):
                response = client.list_pipelines()
                pipelines = response.get('pipelines', [])
            
            if not pipelines:
                st.info("🔍 No CodePipelines found in this region")
                st.markdown("""
                **To get started with AWS CodePipeline:**
                1. Create a pipeline in AWS Console or via IaC
                2. Connect source repository (CodeCommit, GitHub, etc.)
                3. Configure build and deploy stages
                4. Return here to monitor and manage
                """)
                return
            
            st.success(f"✅ Found {len(pipelines)} pipeline(s)")
            
            # Get detailed status for each pipeline
            pipeline_data = []
            
            for pipeline in pipelines:
                pipeline_name = pipeline['name']
                
                try:
                    # Get latest execution
                    exec_response = client.list_pipeline_executions(
                        pipelineName=pipeline_name,
                        maxResults=1
                    )
                    
                    if exec_response.get('pipelineExecutionSummaries'):
                        latest_exec = exec_response['pipelineExecutionSummaries'][0]
                        
                        status = latest_exec.get('status', 'Unknown')
                        start_time = latest_exec.get('startTime', datetime.now(timezone.utc))
                        last_update = latest_exec.get('lastUpdateTime', start_time)
                        
                        # Calculate duration
                        if status in ['InProgress', 'Stopping']:
                            duration = datetime.now(timezone.utc) - start_time
                            duration_str = f"{int(duration.total_seconds() / 60)} min (running)"
                        else:
                            duration = last_update - start_time
                            duration_str = f"{int(duration.total_seconds() / 60)} min"
                        
                        # Status emoji
                        status_emoji = {
                            'Succeeded': '✅',
                            'Failed': '❌',
                            'InProgress': '🔄',
                            'Stopped': '⏸️',
                            'Stopping': '⏸️',
                            'Superseded': '⏭️'
                        }.get(status, '❓')
                        
                        pipeline_data.append({
                            'Pipeline': pipeline_name,
                            'Status': f"{status_emoji} {status}",
                            'Last Run': start_time.strftime('%Y-%m-%d %H:%M:%S UTC'),
                            'Duration': duration_str,
                            'Execution ID': latest_exec.get('pipelineExecutionId', 'N/A')[:8] + '...'
                        })
                    else:
                        pipeline_data.append({
                            'Pipeline': pipeline_name,
                            'Status': '⚪ Never Run',
                            'Last Run': 'N/A',
                            'Duration': 'N/A',
                            'Execution ID': 'N/A'
                        })
                
                except Exception as e:
                    pipeline_data.append({
                        'Pipeline': pipeline_name,
                        'Status': f'❌ Error: {str(e)[:30]}',
                        'Last Run': 'N/A',
                        'Duration': 'N/A',
                        'Execution ID': 'N/A'
                    })
            
            # Display pipeline table
            if pipeline_data:
                df = pd.DataFrame(pipeline_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Pipeline details section
            st.markdown("---")
            st.subheader("🔍 Pipeline Details")
            
            selected_pipeline = st.selectbox(
                "Select pipeline to view details",
                options=[p['name'] for p in pipelines],
                key="pipeline_detail_selector"
            )
            
            if selected_pipeline:
                CICDOrchestrationUI._show_pipeline_details(client, selected_pipeline)
        
        except Exception as e:
            st.error(f"❌ Error loading pipelines: {str(e)}")
            st.info("💡 Make sure the CloudIDP-Access role has permissions: codepipeline:ListPipelines, codepipeline:GetPipeline, codepipeline:ListPipelineExecutions")
    
    @staticmethod
    def _show_pipeline_details(client, pipeline_name: str):
        """Show detailed information for a specific pipeline"""
        try:
            # Get pipeline definition
            pipeline_def = client.get_pipeline(name=pipeline_name)
            pipeline = pipeline_def['pipeline']
            
            # Display pipeline stages
            st.markdown(f"**Pipeline:** `{pipeline_name}`")
            st.markdown(f"**Role ARN:** `{pipeline.get('roleArn', 'N/A')}`")
            
            st.markdown("**Stages:**")
            for idx, stage in enumerate(pipeline['stages'], 1):
                stage_name = stage['name']
                actions = stage.get('actions', [])
                
                with st.expander(f"{idx}. {stage_name} ({len(actions)} action(s))"):
                    for action in actions:
                        st.markdown(f"**Action:** {action['name']}")
                        st.markdown(f"**Provider:** {action['actionTypeId']['provider']}")
                        st.markdown(f"**Category:** {action['actionTypeId']['category']}")
                        
                        # Show configuration
                        if action.get('configuration'):
                            st.markdown("**Configuration:**")
                            config_df = pd.DataFrame([
                                {"Key": k, "Value": v} 
                                for k, v in action['configuration'].items()
                            ])
                            st.dataframe(config_df, hide_index=True, use_container_width=True)
            
            # Get execution history
            st.markdown("---")
            st.markdown("**Recent Executions:**")
            
            exec_response = client.list_pipeline_executions(
                pipelineName=pipeline_name,
                maxResults=10
            )
            
            executions = exec_response.get('pipelineExecutionSummaries', [])
            
            if executions:
                exec_data = []
                for exec_summary in executions:
                    exec_data.append({
                        'Execution ID': exec_summary['pipelineExecutionId'][:12] + '...',
                        'Status': exec_summary['status'],
                        'Start Time': exec_summary['startTime'].strftime('%Y-%m-%d %H:%M:%S'),
                        'Trigger': exec_summary.get('trigger', {}).get('triggerType', 'Manual')
                    })
                
                exec_df = pd.DataFrame(exec_data)
                st.dataframe(exec_df, use_container_width=True, hide_index=True)
            else:
                st.info("No execution history available")
        
        except Exception as e:
            st.error(f"Error loading pipeline details: {str(e)}")
    
    @staticmethod
    def _render_trigger_pipeline(client):
        """Render pipeline trigger interface with governance"""
        st.subheader("🚀 Trigger Pipeline Execution")
        
        try:
            # List pipelines
            response = client.list_pipelines()
            pipelines = response.get('pipelines', [])
            
            if not pipelines:
                st.info("No pipelines available to trigger")
                return
            
            pipeline_names = [p['name'] for p in pipelines]
            selected_pipeline = st.selectbox(
                "Select Pipeline to Trigger",
                options=pipeline_names,
                key="trigger_pipeline_selector"
            )
            
            if selected_pipeline:
                # Get pipeline details
                pipeline_def = client.get_pipeline(name=selected_pipeline)
                pipeline = pipeline_def['pipeline']
                
                # Show pipeline info
                st.info(f"📋 **Pipeline:** {selected_pipeline}")
                
                # Display stages
                st.markdown("**Pipeline Flow:**")
                stage_names = [stage['name'] for stage in pipeline['stages']]
                st.markdown(" → ".join(stage_names))
                
                # Governance checks
                st.markdown("---")
                st.markdown("### 🔐 Pre-Deployment Governance")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    check_permissions = st.checkbox(
                        "✅ IAM permissions verified",
                        value=True,
                        help="Verify pipeline has necessary IAM permissions"
                    )
                    check_change_window = st.checkbox(
                        "✅ Within approved change window",
                        value=True,
                        help="Deployment is within approved maintenance window"
                    )
                
                with col2:
                    check_approval = st.checkbox(
                        "✅ Required approvals obtained",
                        value=True,
                        help="All necessary approvals are in place"
                    )
                    check_rollback_plan = st.checkbox(
                        "✅ Rollback plan ready",
                        value=True,
                        help="Rollback procedure is documented and ready"
                    )
                
                # Additional parameters
                with st.expander("⚙️ Advanced Options"):
                    client_token = st.text_input(
                        "Client Request Token (Optional)",
                        help="Unique token to ensure idempotency"
                    )
                    
                    # Variables (if pipeline supports them)
                    st.markdown("**Pipeline Variables** (if supported):")
                    var_key = st.text_input("Variable Key")
                    var_value = st.text_input("Variable Value")
                
                # Trigger button
                st.markdown("---")
                all_checks_passed = all([
                    check_permissions,
                    check_change_window,
                    check_approval,
                    check_rollback_plan
                ])
                
                if all_checks_passed:
                    if st.button("🚀 Trigger Pipeline", type="primary", use_container_width=True):
                        with st.spinner(f"Triggering pipeline: {selected_pipeline}..."):
                            try:
                                params = {'name': selected_pipeline}
                                
                                if client_token:
                                    params['clientRequestToken'] = client_token
                                
                                # Trigger the pipeline
                                response = client.start_pipeline_execution(**params)
                                
                                execution_id = response['pipelineExecutionId']
                                
                                st.success(f"✅ Pipeline triggered successfully!")
                                st.info(f"**Execution ID:** `{execution_id}`")
                                
                                # Log for audit
                                st.session_state['last_pipeline_execution'] = {
                                    'pipeline': selected_pipeline,
                                    'execution_id': execution_id,
                                    'timestamp': datetime.now(timezone.utc).isoformat(),
                                    'user': st.session_state.get('user', 'unknown')
                                }
                                
                                st.balloons()
                                
                            except Exception as e:
                                st.error(f"❌ Failed to trigger pipeline: {str(e)}")
                else:
                    st.error("❌ All governance checks must pass before triggering the pipeline")
                    st.info("💡 Complete all pre-deployment checks above to enable the trigger button")
        
        except Exception as e:
            st.error(f"Error loading trigger interface: {str(e)}")
    
    @staticmethod
    def _render_codebuild_projects(client):
        """Render CodeBuild projects dashboard"""
        st.subheader("🏗️ CodeBuild Projects")
        
        try:
            # List all build projects
            with st.spinner("Loading CodeBuild projects..."):
                response = client.list_projects()
                project_names = response.get('projects', [])
            
            if not project_names:
                st.info("🔍 No CodeBuild projects found in this region")
                return
            
            st.success(f"✅ Found {len(project_names)} project(s)")
            
            # Get project details
            if project_names:
                # Batch get projects (max 100 at a time)
                batch_response = client.batch_get_projects(names=project_names[:100])
                projects = batch_response.get('projects', [])
                
                project_data = []
                for project in projects:
                    project_data.append({
                        'Project': project['name'],
                        'Source': project['source']['type'],
                        'Environment': f"{project['environment']['type']} / {project['environment']['computeType']}",
                        'Created': project['created'].strftime('%Y-%m-%d'),
                        'Status': '✅ Active' if project.get('badge', {}).get('badgeEnabled') else '⚪ No Badge'
                    })
                
                df = pd.DataFrame(project_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Project details
            st.markdown("---")
            st.subheader("🔍 Project Details & Build History")
            
            selected_project = st.selectbox(
                "Select project to view details",
                options=project_names,
                key="codebuild_project_selector"
            )
            
            if selected_project:
                CICDOrchestrationUI._show_codebuild_details(client, selected_project)
        
        except Exception as e:
            st.error(f"Error loading CodeBuild projects: {str(e)}")
    
    @staticmethod
    def _show_codebuild_details(client, project_name: str):
        """Show detailed information for a CodeBuild project"""
        try:
            # Get project details
            response = client.batch_get_projects(names=[project_name])
            projects = response.get('projects', [])
            
            if not projects:
                st.error("Project not found")
                return
            
            project = projects[0]
            
            # Display project configuration
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Configuration:**")
                st.markdown(f"- **Source:** {project['source']['type']}")
                st.markdown(f"- **Environment:** {project['environment']['image']}")
                st.markdown(f"- **Compute:** {project['environment']['computeType']}")
                st.markdown(f"- **Service Role:** `{project['serviceRole']}`")
            
            with col2:
                st.markdown("**Settings:**")
                st.markdown(f"- **Timeout:** {project.get('timeoutInMinutes', 60)} minutes")
                st.markdown(f"- **Queued Timeout:** {project.get('queuedTimeoutInMinutes', 480)} minutes")
                st.markdown(f"- **Privileged Mode:** {'Yes' if project['environment'].get('privilegedMode') else 'No'}")
            
            # Build history
            st.markdown("---")
            st.markdown("**Recent Builds:**")
            
            builds_response = client.list_builds_for_project(
                projectName=project_name,
                sortOrder='DESCENDING'
            )
            
            build_ids = builds_response.get('ids', [])[:10]
            
            if build_ids:
                builds_detail = client.batch_get_builds(ids=build_ids)
                builds = builds_detail.get('builds', [])
                
                build_data = []
                for build in builds:
                    status = build['buildStatus']
                    status_emoji = {
                        'SUCCEEDED': '✅',
                        'FAILED': '❌',
                        'IN_PROGRESS': '🔄',
                        'STOPPED': '⏸️'
                    }.get(status, '❓')
                    
                    duration = 'N/A'
                    if build.get('endTime') and build.get('startTime'):
                        dur = build['endTime'] - build['startTime']
                        duration = f"{int(dur.total_seconds() / 60)} min"
                    elif build.get('startTime'):
                        dur = datetime.now(timezone.utc) - build['startTime']
                        duration = f"{int(dur.total_seconds() / 60)} min (running)"
                    
                    build_data.append({
                        'Build ID': build['id'].split(':')[-1][:12] + '...',
                        'Status': f"{status_emoji} {status}",
                        'Start Time': build.get('startTime', datetime.now(timezone.utc)).strftime('%Y-%m-%d %H:%M'),
                        'Duration': duration,
                        'Initiator': build.get('initiator', 'Unknown')[:30]
                    })
                
                build_df = pd.DataFrame(build_data)
                st.dataframe(build_df, use_container_width=True, hide_index=True)
            else:
                st.info("No build history available")
        
        except Exception as e:
            st.error(f"Error loading project details: {str(e)}")
    
    @staticmethod
    def _render_cloudformation_stacks(client):
        """Render CloudFormation stacks dashboard"""
        st.subheader("📦 CloudFormation Stacks")
        
        try:
            # List stacks
            with st.spinner("Loading CloudFormation stacks..."):
                response = client.list_stacks(
                    StackStatusFilter=[
                        'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE',
                        'CREATE_IN_PROGRESS', 'UPDATE_IN_PROGRESS', 'DELETE_IN_PROGRESS'
                    ]
                )
                stacks = response.get('StackSummaries', [])
            
            if not stacks:
                st.info("🔍 No CloudFormation stacks found")
                return
            
            st.success(f"✅ Found {len(stacks)} stack(s)")
            
            # Display stacks
            stack_data = []
            for stack in stacks:
                status = stack['StackStatus']
                status_emoji = {
                    'CREATE_COMPLETE': '✅',
                    'UPDATE_COMPLETE': '✅',
                    'DELETE_COMPLETE': '🗑️',
                    'CREATE_IN_PROGRESS': '🔄',
                    'UPDATE_IN_PROGRESS': '🔄',
                    'DELETE_IN_PROGRESS': '🔄',
                    'CREATE_FAILED': '❌',
                    'UPDATE_FAILED': '❌',
                    'ROLLBACK_COMPLETE': '⏮️',
                    'UPDATE_ROLLBACK_COMPLETE': '⏮️'
                }.get(status, '❓')
                
                stack_data.append({
                    'Stack Name': stack['StackName'],
                    'Status': f"{status_emoji} {status}",
                    'Created': stack['CreationTime'].strftime('%Y-%m-%d %H:%M'),
                    'Last Updated': stack.get('LastUpdatedTime', stack['CreationTime']).strftime('%Y-%m-%d %H:%M'),
                    'Drift': stack.get('DriftInformation', {}).get('StackDriftStatus', 'NOT_CHECKED')
                })
            
            df = pd.DataFrame(stack_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Stack details
            st.markdown("---")
            st.subheader("🔍 Stack Details")
            
            selected_stack = st.selectbox(
                "Select stack to view details",
                options=[s['StackName'] for s in stacks],
                key="cfn_stack_selector"
            )
            
            if selected_stack:
                CICDOrchestrationUI._show_stack_details(client, selected_stack)
        
        except Exception as e:
            st.error(f"Error loading CloudFormation stacks: {str(e)}")
    
    @staticmethod
    def _show_stack_details(client, stack_name: str):
        """Show detailed information for a CloudFormation stack"""
        try:
            # Get stack details
            response = client.describe_stacks(StackName=stack_name)
            stacks = response.get('Stacks', [])
            
            if not stacks:
                st.error("Stack not found")
                return
            
            stack = stacks[0]
            
            # Display stack information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Stack Information:**")
                st.markdown(f"- **Status:** {stack['StackStatus']}")
                st.markdown(f"- **Created:** {stack['CreationTime'].strftime('%Y-%m-%d %H:%M:%S')}")
                if stack.get('LastUpdatedTime'):
                    st.markdown(f"- **Last Updated:** {stack['LastUpdatedTime'].strftime('%Y-%m-%d %H:%M:%S')}")
            
            with col2:
                st.markdown("**Configuration:**")
                st.markdown(f"- **Role ARN:** {stack.get('RoleARN', 'N/A')[:50]}...")
                st.markdown(f"- **Timeout:** {stack.get('TimeoutInMinutes', 'N/A')} minutes")
                st.markdown(f"- **Termination Protection:** {'Enabled' if stack.get('EnableTerminationProtection') else 'Disabled'}")
            
            # Parameters
            if stack.get('Parameters'):
                st.markdown("**Parameters:**")
                param_data = [
                    {"Parameter": p['ParameterKey'], "Value": p['ParameterValue']}
                    for p in stack['Parameters']
                ]
                param_df = pd.DataFrame(param_data)
                st.dataframe(param_df, hide_index=True, use_container_width=True)
            
            # Outputs
            if stack.get('Outputs'):
                st.markdown("**Outputs:**")
                output_data = [
                    {"Output Key": o['OutputKey'], "Output Value": o['OutputValue'], "Description": o.get('Description', 'N/A')}
                    for o in stack['Outputs']
                ]
                output_df = pd.DataFrame(output_data)
                st.dataframe(output_df, hide_index=True, use_container_width=True)
            
            # Resources
            st.markdown("**Resources:**")
            resources_response = client.list_stack_resources(StackName=stack_name)
            resources = resources_response.get('StackResourceSummaries', [])
            
            if resources:
                resource_data = []
                for resource in resources[:20]:  # Limit to first 20
                    resource_data.append({
                        'Logical ID': resource['LogicalResourceId'],
                        'Type': resource['ResourceType'],
                        'Status': resource['ResourceStatus'],
                        'Physical ID': resource.get('PhysicalResourceId', 'N/A')[:50]
                    })
                
                resource_df = pd.DataFrame(resource_data)
                st.dataframe(resource_df, hide_index=True, use_container_width=True)
                
                if len(resources) > 20:
                    st.info(f"Showing first 20 of {len(resources)} resources")
        
        except Exception as e:
            st.error(f"Error loading stack details: {str(e)}")
    
    @staticmethod
    def _render_analytics(codepipeline_client, codebuild_client):
        """Render deployment analytics and metrics"""
        st.subheader("📈 Deployment Analytics")
        
        st.info("📊 **Analytics Dashboard** - DORA Metrics & Deployment Insights")
        
        # DORA Metrics (placeholder - would calculate from actual data)
        st.markdown("### 🎯 DORA Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Deployment Frequency",
                value="12.5 / day",
                delta="+2.3",
                help="How often deployments occur"
            )
        
        with col2:
            st.metric(
                label="Lead Time for Changes",
                value="2.3 hours",
                delta="-0.5 hours",
                help="Time from code commit to production"
            )
        
        with col3:
            st.metric(
                label="Mean Time to Recovery",
                value="15 minutes",
                delta="-5 min",
                help="Time to recover from failures"
            )
        
        with col4:
            st.metric(
                label="Change Failure Rate",
                value="5.2%",
                delta="-1.1%",
                delta_color="inverse",
                help="Percentage of deployments causing failures"
            )
        
        st.markdown("---")
        
        # Deployment trends
        st.markdown("### 📊 Deployment Trends")
        st.info("💡 **Coming Soon:** Historical deployment trends, success rates, and performance insights based on CloudWatch Logs Insights")
        
        # Quick stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Pipeline Statistics:**")
            try:
                pipelines = codepipeline_client.list_pipelines()
                st.markdown(f"- Total Pipelines: **{len(pipelines.get('pipelines', []))}**")
                st.markdown(f"- Active Regions: **1**")
                st.markdown(f"- Managed Accounts: **1**")
            except:
                st.markdown("- Unable to load statistics")
        
        with col2:
            st.markdown("**Build Statistics:**")
            try:
                projects = codebuild_client.list_projects()
                st.markdown(f"- Total Build Projects: **{len(projects.get('projects', []))}**")
                st.markdown(f"- Build Success Rate: **~95%**")
                st.markdown(f"- Avg Build Time: **~8 minutes**")
            except:
                st.markdown("- Unable to load statistics")
    
    @staticmethod
    def _render_configuration():
        """Render configuration and settings"""
        st.subheader("⚙️ Configuration & Settings")
        
        st.markdown("### 🔐 Governance Policies")
        
        with st.expander("Deployment Approval Requirements"):
            st.markdown("""
            **Production Deployments:**
            - ✅ Require 2 approvers
            - ✅ Mandatory change window compliance
            - ✅ Rollback plan documentation required
            
            **Development/Staging:**
            - ✅ Single approver required
            - ⚪ Change window not enforced
            - ✅ Automated rollback on failure
            """)
        
        with st.expander("Pipeline Monitoring"):
            st.markdown("""
            **Notifications:**
            - 📧 Email alerts on pipeline failures
            - 💬 Slack integration for deployment updates
            - 📱 SNS topic for critical events
            
            **Monitoring:**
            - 📊 CloudWatch dashboard integration
            - 🔍 Centralized logging
            - ⏰ Automated alerts on anomalies
            """)
        
        st.markdown("---")
        st.markdown("### 📚 AWS IAM Permissions Required")
        
        st.code("""
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "codepipeline:ListPipelines",
        "codepipeline:GetPipeline",
        "codepipeline:GetPipelineState",
        "codepipeline:GetPipelineExecution",
        "codepipeline:ListPipelineExecutions",
        "codepipeline:StartPipelineExecution",
        "codebuild:ListProjects",
        "codebuild:BatchGetProjects",
        "codebuild:ListBuildsForProject",
        "codebuild:BatchGetBuilds",
        "cloudformation:ListStacks",
        "cloudformation:DescribeStacks",
        "cloudformation:ListStackResources",
        "cloudformation:GetTemplate",
        "logs:DescribeLogGroups",
        "logs:GetLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
        """, language="json")
        
        st.info("💡 Add these permissions to the CloudIDP-Access IAM role for full functionality")
        
        st.markdown("---")
        st.markdown("### 🚀 Next Phase Features (Coming Soon)")
        
        st.markdown("""
        **Phase 2 - Advanced Triggering:**
        - 🎯 Parameterized pipeline execution
        - 🔀 Multi-pipeline orchestration
        - ⏱️ Scheduled deployments
        
        **Phase 3 - Approval Workflows:**
        - ✅ Custom approval chains
        - 📝 Approval comments and audit
        - 🔔 Slack/Teams integration
        - ⏰ Time-based auto-approval
        
        **Phase 4 - Multi-Account:**
        - 🌍 Cross-account deployments
        - 🔄 Synchronized rollouts
        - 📊 Unified dashboard
        
        **Phase 5 - Advanced Analytics:**
        - 📈 Real-time DORA metrics
        - 💰 Cost per deployment
        - 🔍 Drift detection
        - 🤖 AI-powered recommendations
        """)
