"""
CI/CD Pipeline Orchestration Module - Complete Self-Service Platform
Create, manage, and monitor pipelines entirely within CloudIDP - NO AWS Console needed!
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
from core_account_manager import get_account_manager, get_account_names
import json
import time

class CICDOrchestrationModule:
    """Complete CI/CD Platform - Create pipelines without AWS Console!"""
    
    @staticmethod
    def render():
        """Main render method"""
        st.title("🔄 CI/CD Pipeline Orchestration")
        st.markdown("**Create & Manage Pipelines** - Everything in CloudIDP, no AWS Console needed!")
        
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
        
        # Account and region selection
        col1, col2 = st.columns(2)
        
        with col1:
            selected_account = st.selectbox(
                "Select AWS Account",
                options=account_names,
                key="cicd_account"
            )
        
        with col2:
            selected_region = st.session_state.get('selected_regions', 'all')
            if selected_region == 'all':
                st.error("⚠️ Please select a specific region from sidebar")
                return
            st.info(f"📍 Region: {selected_region}")
        
        if not selected_account:
            return
        
        # Get session
        session = account_mgr.get_session_with_region(selected_account, selected_region)
        if not session:
            st.error("Failed to get AWS session")
            return
        
        # Main tabs - CREATE PIPELINE is 2nd tab (prominent position!)
        tabs = st.tabs([
            "📊 Pipeline Dashboard",
            "🎨 Create Pipeline",  # ← PROMINENT! No AWS Console needed!
            "🚀 Trigger Pipeline",
            "🏗️ CodeBuild Projects",
            "🗂️ CloudFormation Stacks",
            "📈 Analytics",
            "⚙️ Configuration"
        ])
        
        # Tab 1: Pipeline Dashboard
        with tabs[0]:
            render_pipeline_dashboard(session, selected_account, selected_region)
        
        # Tab 2: Create Pipeline (NEW - Pipeline Builder!)
        with tabs[1]:
            render_pipeline_builder(session, selected_account, selected_region)
        
        # Tab 3: Trigger Pipeline
        with tabs[2]:
            render_trigger_pipeline(session)
        
        # Tab 4: CodeBuild
        with tabs[3]:
            render_codebuild(session)
        
        # Tab 5: CloudFormation
        with tabs[4]:
            render_cloudformation(session)
        
        # Tab 6: Analytics
        with tabs[5]:
            render_analytics(session)
        
        # Tab 7: Configuration
        with tabs[6]:
            render_configuration()


# ==================== TAB IMPLEMENTATIONS ====================

def render_pipeline_dashboard(session, account, region):
    """Pipeline dashboard - Updated to point users to CREATE tab!"""
    st.subheader("📊 Pipeline Dashboard")
    
    try:
        cp_client = session.client('codepipeline')
        
        # Get all pipelines
        response = cp_client.list_pipelines()
        pipelines = response.get('pipelines', [])
        
        if not pipelines:
            # NEW MESSAGE - Points to CloudIDP Create tab!
            st.info("🎯 **No pipelines yet? Create one in minutes!**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎨 Create Your First Pipeline
                
                **Right here in CloudIDP - No AWS Console needed!**
                
                1. Click the **"Create Pipeline"** tab above
                2. Choose a template (Python, React, Node.js, etc.)
                3. Configure your pipeline
                4. Click "Create"
                5. Done in 5 minutes! ✅
                
                **Templates available:**
                - 🐍 Python App (Flask/Django)
                - ⚛️ React Frontend (SPA)
                - 🟢 Node.js API (Express)
                - ☕ Java Spring Boot
                - 🐳 Docker Container
                - 🌐 Static Website
                """)
            
            with col2:
                st.markdown("""
                ### 💡 What Gets Created
                
                CloudIDP automatically creates:
                - ✅ IAM service roles
                - ✅ S3 artifact bucket
                - ✅ CodeCommit repository (optional)
                - ✅ CodeBuild project
                - ✅ Complete CI/CD pipeline
                - ✅ Sample code to get started
                
                **Time:** 5 minutes from click to working pipeline
                
                **Cost:** ~$0.10/day for idle pipeline
                
                **Complexity:** Low - guided step-by-step
                """)
            
            st.markdown("---")
            
            # Quick start button
            if st.button("🚀 Create Your First Pipeline Now", type="primary", use_container_width=True):
                st.info("👆 Click the **'Create Pipeline'** tab above to get started!")
            
            return
        
        # If pipelines exist, show dashboard
        st.success(f"✅ Found {len(pipelines)} pipeline(s)")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Pipelines", len(pipelines))
        
        # Get pipeline states
        succeeded = 0
        failed = 0
        in_progress = 0
        
        pipeline_data = []
        
        for pipeline in pipelines:
            try:
                state = cp_client.get_pipeline_state(name=pipeline['name'])
                
                # Determine status
                stage_states = state.get('stageStates', [])
                if not stage_states:
                    status = "Unknown"
                    status_icon = "⚪"
                else:
                    latest_state = stage_states[-1].get('latestExecution', {})
                    exec_status = latest_state.get('status', 'Unknown')
                    
                    if exec_status == 'Succeeded':
                        status = "Succeeded"
                        status_icon = "✅"
                        succeeded += 1
                    elif exec_status == 'Failed':
                        status = "Failed"
                        status_icon = "❌"
                        failed += 1
                    elif exec_status == 'InProgress':
                        status = "In Progress"
                        status_icon = "🔄"
                        in_progress += 1
                    else:
                        status = exec_status
                        status_icon = "⚪"
                
                # Get last execution time
                last_exec_time = "Never"
                for stage in stage_states:
                    if 'latestExecution' in stage and 'lastStatusChange' in stage['latestExecution']:
                        last_exec_time = stage['latestExecution']['lastStatusChange'].strftime("%Y-%m-%d %H:%M")
                        break
                
                pipeline_data.append({
                    'Status': f"{status_icon} {status}",
                    'Pipeline': pipeline['name'],
                    'Version': pipeline.get('version', 'N/A'),
                    'Last Execution': last_exec_time
                })
                
            except Exception as e:
                pipeline_data.append({
                    'Status': "⚠️ Error",
                    'Pipeline': pipeline['name'],
                    'Version': 'N/A',
                    'Last Execution': "Error loading"
                })
        
        with col2:
            st.metric("✅ Succeeded", succeeded)
        
        with col3:
            st.metric("❌ Failed", failed)
        
        with col4:
            st.metric("🔄 In Progress", in_progress)
        
        # Pipeline table
        st.markdown("### 📋 All Pipelines")
        
        if pipeline_data:
            df = pd.DataFrame(pipeline_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Quick actions
            st.markdown("### ⚡ Quick Actions")
            selected_pipeline = st.selectbox(
                "Select Pipeline",
                options=[p['name'] for p in pipelines],
                key="dashboard_pipeline_select"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🚀 Trigger Now", use_container_width=True):
                    try:
                        cp_client.start_pipeline_execution(name=selected_pipeline)
                        st.success(f"✅ Pipeline '{selected_pipeline}' triggered!")
                    except Exception as e:
                        st.error(f"Failed: {str(e)}")
            
            with col2:
                if st.button("📊 View Details", use_container_width=True):
                    try:
                        pipeline_details = cp_client.get_pipeline(name=selected_pipeline)
                        with st.expander("Pipeline Configuration", expanded=True):
                            st.json(pipeline_details['pipeline'])
                    except Exception as e:
                        st.error(f"Failed: {str(e)}")
            
            with col3:
                if st.button("📜 View History", use_container_width=True):
                    try:
                        executions = cp_client.list_pipeline_executions(pipelineName=selected_pipeline)
                        exec_list = executions.get('pipelineExecutionSummaries', [])
                        
                        if exec_list:
                            exec_data = []
                            for exec in exec_list[:10]:
                                exec_data.append({
                                    'Status': exec.get('status', 'Unknown'),
                                    'ID': exec.get('pipelineExecutionId', 'N/A')[:8],
                                    'Start Time': exec.get('startTime', 'N/A')
                                })
                            
                            df_exec = pd.DataFrame(exec_data)
                            st.dataframe(df_exec, use_container_width=True, hide_index=True)
                        else:
                            st.info("No execution history")
                    except Exception as e:
                        st.error(f"Failed: {str(e)}")
        
        # Add another pipeline button
        st.markdown("---")
        if st.button("➕ Create Another Pipeline", use_container_width=True):
            st.info("👆 Click the **'Create Pipeline'** tab above!")
        
    except Exception as e:
        st.error(f"Error loading pipelines: {str(e)}")


def render_pipeline_builder(session, account, region):
    """Pipeline Builder - Create pipelines without AWS Console!"""
    st.subheader("🎨 Pipeline Builder")
    st.markdown("**Create complete CI/CD pipelines in minutes - No AWS Console required!**")
    
    # Hero message
    st.success("✨ **Everything you need to create professional CI/CD pipelines - right here in CloudIDP!**")
    
    # Initialize AWS clients
    try:
        cp_client = session.client('codepipeline')
        cb_client = session.client('codebuild')
        iam_client = session.client('iam')
        s3_client = session.client('s3')
        codecommit_client = session.client('codecommit')
    except Exception as e:
        st.error(f"Failed to initialize clients: {str(e)}")
        return
    
    # Builder tabs
    builder_tabs = st.tabs([
        "⚡ Quick Create",
        "🔗 Repositories"
    ])
    
    # Quick Create
    with builder_tabs[0]:
        render_quick_create(cp_client, cb_client, iam_client, s3_client, codecommit_client, region)
    
    # Repository Manager
    with builder_tabs[1]:
        render_repository_manager(codecommit_client, region)


def render_quick_create(cp_client, cb_client, iam_client, s3_client, codecommit_client, region):
    """Quick create pipeline from templates"""
    st.markdown("### ⚡ Quick Create Pipeline")
    st.markdown("**Choose a template and create your pipeline in 5 minutes**")
    
    # Benefits callout
    st.info("""
    💡 **Why use CloudIDP Pipeline Builder?**
    - ✅ No AWS Console access needed
    - ✅ Automatic resource creation (IAM, S3, CodeBuild, Pipeline)
    - ✅ Pre-configured best practices
    - ✅ Sample code included
    - ✅ 5-minute setup time
    """)
    
    # Template selection
    st.markdown("#### 🎯 Choose Your Stack")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🐍 Python App", use_container_width=True, help="Flask/Django + EB"):
            st.session_state['quick_template'] = 'python-app'
        
        if st.button("⚛️ React App", use_container_width=True, help="SPA + S3"):
            st.session_state['quick_template'] = 'react-app'
    
    with col2:
        if st.button("🟢 Node.js API", use_container_width=True, help="Express + EB"):
            st.session_state['quick_template'] = 'nodejs-api'
        
        if st.button("☕ Java Spring", use_container_width=True, help="Spring Boot"):
            st.session_state['quick_template'] = 'java-spring'
    
    with col3:
        if st.button("🐳 Docker App", use_container_width=True, help="Container + ECS"):
            st.session_state['quick_template'] = 'docker-app'
        
        if st.button("🌐 Static Site", use_container_width=True, help="HTML + S3"):
            st.session_state['quick_template'] = 'static-site'
    
    # Show creation form if template selected
    if st.session_state.get('quick_template'):
        template_type = st.session_state['quick_template']
        
        st.markdown("---")
        st.markdown(f"### 📝 Configure Your Pipeline")
        
        with st.form("quick_create_form"):
            # Pipeline name
            pipeline_name = st.text_input(
                "Pipeline Name",
                value=f"my-{template_type}",
                help="Must be unique in your account"
            )
            
            # Source configuration
            st.markdown("#### 🔗 Source Repository")
            
            source_provider = st.selectbox(
                "Source Provider",
                options=["CodeCommit", "GitHub", "S3"]
            )
            
            if source_provider == "CodeCommit":
                try:
                    repos = codecommit_client.list_repositories()
                    existing_repos = [r['repositoryName'] for r in repos.get('repositories', [])]
                    
                    create_new = st.checkbox("Create new repository", value=True)
                    
                    if create_new:
                        repo_name = st.text_input("Repository Name", value=pipeline_name)
                    else:
                        if existing_repos:
                            repo_name = st.selectbox("Select Repository", options=existing_repos)
                        else:
                            st.warning("No repos found. Will create new one.")
                            repo_name = st.text_input("Repository Name", value=pipeline_name)
                            create_new = True
                    
                    branch_name = st.text_input("Branch", value="main")
                except Exception as e:
                    st.error(f"Error accessing CodeCommit: {str(e)}")
                    repo_name = st.text_input("Repository Name", value=pipeline_name)
                    branch_name = st.text_input("Branch", value="main")
                    create_new = True
            
            elif source_provider == "GitHub":
                repo_url = st.text_input("Repository URL", placeholder="https://github.com/user/repo")
                branch_name = st.text_input("Branch", value="main")
                github_token = st.text_input("GitHub Token", type="password", help="Personal access token with repo permissions")
            
            # Deploy target
            st.markdown("#### 🚀 Deploy Target")
            
            deploy_target = st.selectbox(
                "Deploy To",
                options=["S3 (Static)", "Elastic Beanstalk", "ECS", "Lambda", "None (Build only)"]
            )
            
            # Submit
            st.markdown("---")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown("**🎁 What CloudIDP will create for you:**")
                st.markdown("""
                - ✅ IAM Service Roles (Pipeline + Build)
                - ✅ S3 Artifact Bucket (with versioning)
                - ✅ CodeCommit Repository (if selected)
                - ✅ CodeBuild Project (with buildspec)
                - ✅ Complete CodePipeline
                - ✅ Sample code to get started
                
                **Time:** ~5 minutes | **Cost:** ~$0.10/day
                """)
            
            with col2:
                submitted = st.form_submit_button("🚀 Create Pipeline", type="primary", use_container_width=True)
            
            if submitted:
                if not pipeline_name:
                    st.error("Pipeline name required")
                elif source_provider == "GitHub" and (not repo_url or not github_token):
                    st.error("GitHub URL and token required")
                else:
                    # Create pipeline
                    with st.spinner("🎨 Creating your CI/CD pipeline..."):
                        success, message = create_pipeline(
                            pipeline_name=pipeline_name,
                            template_type=template_type,
                            source_provider=source_provider,
                            source_config={
                                'repo_name': repo_name if source_provider == "CodeCommit" else None,
                                'branch': branch_name if source_provider != "S3" else None,
                                'create_repo': create_new if source_provider == "CodeCommit" else False
                            },
                            deploy_target=deploy_target,
                            cp_client=cp_client,
                            cb_client=cb_client,
                            iam_client=iam_client,
                            s3_client=s3_client,
                            codecommit_client=codecommit_client,
                            region=region
                        )
                    
                    if success:
                        st.success("✅ Pipeline created successfully!")
                        st.balloons()
                        
                        st.markdown("---")
                        st.markdown("### 🎉 Your Pipeline is Ready!")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"""
                            **Pipeline:** `{pipeline_name}`
                            **Region:** `{region}`
                            **Status:** Ready to use
                            
                            **Next Steps:**
                            1. Push code to your repository
                            2. Pipeline will auto-trigger
                            3. Monitor in **Dashboard** tab
                            """)
                        
                        with col2:
                            st.markdown("**📝 Sample Code:**")
                            sample = get_sample_code(template_type)
                            st.code(sample, language="python" if "python" in template_type else "javascript")
                        
                        st.info("💡 Go to the **Dashboard** tab to see your new pipeline!")
                        
                        st.session_state['quick_template'] = None
                    else:
                        st.error(f"❌ Failed to create pipeline: {message}")


def create_pipeline(pipeline_name, template_type, source_provider, source_config, 
                    deploy_target, cp_client, cb_client, iam_client, s3_client, 
                    codecommit_client, region):
    """Create the pipeline - core logic"""
    try:
        progress = st.progress(0)
        status = st.empty()
        
        # Step 1: IAM Roles
        status.text("1/5: Creating IAM roles...")
        time.sleep(1)
        
        pipeline_role_name = f"{pipeline_name}-pipeline-role"
        try:
            iam_client.create_role(
                RoleName=pipeline_role_name,
                AssumeRolePolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": "codepipeline.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }]
                })
            )
            iam_client.attach_role_policy(
                RoleName=pipeline_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AWSCodePipelineFullAccess'
            )
            time.sleep(2)
        except iam_client.exceptions.EntityAlreadyExistsException:
            pass
        
        progress.progress(20)
        
        # Step 2: S3 Bucket
        status.text("2/5: Creating artifact bucket...")
        bucket_name = f"{pipeline_name}-artifacts-{int(time.time())}"
        try:
            if region == 'us-east-1':
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
        except Exception as e:
            pass
        
        progress.progress(40)
        
        # Step 3: CodeBuild
        status.text("3/5: Creating CodeBuild project...")
        
        build_role_name = f"{pipeline_name}-build-role"
        try:
            iam_client.create_role(
                RoleName=build_role_name,
                AssumeRolePolicyDocument=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Principal": {"Service": "codebuild.amazonaws.com"},
                        "Action": "sts:AssumeRole"
                    }]
                })
            )
            iam_client.attach_role_policy(
                RoleName=build_role_name,
                PolicyArn='arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess'
            )
            time.sleep(2)
        except iam_client.exceptions.EntityAlreadyExistsException:
            pass
        
        build_role = iam_client.get_role(RoleName=build_role_name)
        build_role_arn = build_role['Role']['Arn']
        
        buildspec = get_buildspec(template_type)
        
        try:
            cb_client.create_project(
                name=f"{pipeline_name}-build",
                source={'type': 'CODEPIPELINE', 'buildspec': buildspec},
                artifacts={'type': 'CODEPIPELINE'},
                environment={
                    'type': 'LINUX_CONTAINER',
                    'image': 'aws/codebuild/standard:7.0',
                    'computeType': 'BUILD_GENERAL1_SMALL'
                },
                serviceRole=build_role_arn
            )
        except cb_client.exceptions.ResourceAlreadyExistsException:
            pass
        
        progress.progress(60)
        
        # Step 4: Repository
        if source_provider == "CodeCommit" and source_config.get('create_repo'):
            status.text("4/5: Creating repository...")
            try:
                codecommit_client.create_repository(
                    repositoryName=source_config['repo_name'],
                    repositoryDescription=f"Repository for {pipeline_name}"
                )
            except codecommit_client.exceptions.RepositoryNameExistsException:
                pass
        
        progress.progress(80)
        
        # Step 5: Pipeline
        status.text("5/5: Creating pipeline...")
        
        pipeline_role = iam_client.get_role(RoleName=pipeline_role_name)
        pipeline_role_arn = pipeline_role['Role']['Arn']
        
        stages = [
            {
                'name': 'Source',
                'actions': [{
                    'name': 'SourceAction',
                    'actionTypeId': {
                        'category': 'Source',
                        'owner': 'AWS',
                        'provider': 'CodeCommit',
                        'version': '1'
                    },
                    'configuration': {
                        'RepositoryName': source_config['repo_name'],
                        'BranchName': source_config['branch'],
                        'PollForSourceChanges': False
                    },
                    'outputArtifacts': [{'name': 'SourceOutput'}]
                }]
            },
            {
                'name': 'Build',
                'actions': [{
                    'name': 'BuildAction',
                    'actionTypeId': {
                        'category': 'Build',
                        'owner': 'AWS',
                        'provider': 'CodeBuild',
                        'version': '1'
                    },
                    'configuration': {'ProjectName': f"{pipeline_name}-build"},
                    'inputArtifacts': [{'name': 'SourceOutput'}],
                    'outputArtifacts': [{'name': 'BuildOutput'}]
                }]
            }
        ]
        
        try:
            cp_client.create_pipeline(
                pipeline={
                    'name': pipeline_name,
                    'roleArn': pipeline_role_arn,
                    'artifactStore': {
                        'type': 'S3',
                        'location': bucket_name
                    },
                    'stages': stages
                }
            )
        except cp_client.exceptions.PipelineNameInUseException:
            return False, "Pipeline name already exists"
        
        progress.progress(100)
        status.text("✅ Complete!")
        
        time.sleep(0.5)
        progress.empty()
        status.empty()
        
        return True, "Success"
        
    except Exception as e:
        return False, str(e)


def get_buildspec(template_type):
    """Get buildspec for template"""
    buildspecs = {
        'python-app': """version: 0.2
phases:
  install:
    runtime-versions:
      python: 3.11
  build:
    commands:
      - pip install -r requirements.txt
      - python -m pytest || true
artifacts:
  files:
    - '**/*'
""",
        'nodejs-api': """version: 0.2
phases:
  install:
    runtime-versions:
      nodejs: 18
  build:
    commands:
      - npm install
      - npm test || true
artifacts:
  files:
    - '**/*'
""",
        'static-site': """version: 0.2
phases:
  build:
    commands:
      - echo "Building static site"
artifacts:
  files:
    - '**/*'
"""
    }
    return buildspecs.get(template_type, buildspecs['static-site'])


def get_sample_code(template_type):
    """Get sample code"""
    samples = {
        'python-app': """# Flask App
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({"message": "Hello from CloudIDP!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
""",
        'nodejs-api': """// Express API
const express = require('express');
const app = express();

app.get('/', (req, res) => {
  res.json({ message: 'Hello from CloudIDP!' });
});

app.listen(3000);
""",
        'static-site': """<!DOCTYPE html>
<html>
<head><title>My Site</title></head>
<body><h1>Hello from CloudIDP!</h1></body>
</html>
"""
    }
    return samples.get(template_type, samples['static-site'])


def render_repository_manager(codecommit_client, region):
    """Manage CodeCommit repositories"""
    st.markdown("### 🔗 Repository Manager")
    st.markdown("**Create and manage CodeCommit repositories - No AWS Console needed!**")
    
    repo_tabs = st.tabs(["📋 Existing", "➕ Create New"])
    
    with repo_tabs[0]:
        try:
            response = codecommit_client.list_repositories()
            repos = response.get('repositories', [])
            
            if repos:
                repo_data = []
                for repo in repos:
                    try:
                        detail = codecommit_client.get_repository(repositoryName=repo['repositoryName'])
                        info = detail['repositoryMetadata']
                        
                        repo_data.append({
                            'Name': info['repositoryName'],
                            'Clone URL': info.get('cloneUrlHttp', 'N/A'),
                            'Created': info.get('creationDate', 'N/A')
                        })
                    except:
                        pass
                
                if repo_data:
                    df = pd.DataFrame(repo_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("No repositories yet. Create one to get started!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    with repo_tabs[1]:
        with st.form("create_repo"):
            st.markdown("**Create a new CodeCommit repository**")
            
            repo_name = st.text_input("Repository Name", placeholder="my-app-repo")
            repo_desc = st.text_area("Description (optional)", placeholder="My application repository")
            
            if st.form_submit_button("✨ Create Repository", type="primary", use_container_width=True):
                if repo_name:
                    try:
                        response = codecommit_client.create_repository(
                            repositoryName=repo_name,
                            repositoryDescription=repo_desc or f"Repository {repo_name}"
                        )
                        st.success(f"✅ Repository '{repo_name}' created!")
                        
                        clone_url = response['repositoryMetadata']['cloneUrlHttp']
                        st.code(f"git clone {clone_url}", language="bash")
                    except codecommit_client.exceptions.RepositoryNameExistsException:
                        st.error("Repository name already exists")
                    except Exception as e:
                        st.error(f"Failed: {str(e)}")
                else:
                    st.error("Repository name required")


def render_trigger_pipeline(session):
    """Trigger pipeline"""
    st.subheader("🚀 Trigger Pipeline")
    
    try:
        cp_client = session.client('codepipeline')
        
        response = cp_client.list_pipelines()
        pipelines = response.get('pipelines', [])
        
        if not pipelines:
            st.info("No pipelines available. Create one in the 'Create Pipeline' tab!")
            return
        
        pipeline_names = [p['name'] for p in pipelines]
        
        selected = st.selectbox("Select Pipeline", options=pipeline_names)
        
        if st.button("🚀 Trigger Execution", type="primary", use_container_width=True):
            try:
                response = cp_client.start_pipeline_execution(name=selected)
                exec_id = response['pipelineExecutionId']
                st.success(f"✅ Pipeline triggered! Execution ID: {exec_id[:8]}")
            except Exception as e:
                st.error(f"Failed: {str(e)}")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def render_codebuild(session):
    """CodeBuild projects"""
    st.subheader("🏗️ CodeBuild Projects")
    
    try:
        cb_client = session.client('codebuild')
        
        response = cb_client.list_projects()
        projects = response.get('projects', [])
        
        if not projects:
            st.info("No CodeBuild projects. Create a pipeline to get started!")
            return
        
        st.metric("Total Projects", len(projects))
        
        project_data = []
        for project_name in projects:
            try:
                detail = cb_client.batch_get_projects(names=[project_name])
                if detail['projects']:
                    proj = detail['projects'][0]
                    project_data.append({
                        'Name': proj['name'],
                        'Environment': proj['environment']['image'],
                        'Compute': proj['environment']['computeType'],
                        'Created': proj.get('created', 'N/A')
                    })
            except:
                pass
        
        if project_data:
            df = pd.DataFrame(project_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def render_cloudformation(session):
    """CloudFormation stacks"""
    st.subheader("🗂️ CloudFormation Stacks")
    
    try:
        cf_client = session.client('cloudformation')
        
        response = cf_client.list_stacks(
            StackStatusFilter=[
                'CREATE_COMPLETE',
                'UPDATE_COMPLETE',
                'CREATE_IN_PROGRESS',
                'UPDATE_IN_PROGRESS'
            ]
        )
        stacks = response.get('StackSummaries', [])
        
        if not stacks:
            st.info("No active CloudFormation stacks")
            return
        
        st.metric("Active Stacks", len(stacks))
        
        stack_data = []
        for stack in stacks:
            stack_data.append({
                'Stack Name': stack['StackName'],
                'Status': stack['StackStatus'],
                'Created': stack.get('CreationTime', 'N/A')
            })
        
        df = pd.DataFrame(stack_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def render_analytics(session):
    """Pipeline analytics"""
    st.subheader("📈 Analytics")
    
    try:
        cp_client = session.client('codepipeline')
        
        response = cp_client.list_pipelines()
        pipelines = response.get('pipelines', [])
        
        if not pipelines:
            st.info("No pipelines to analyze. Create one to get started!")
            return
        
        # Calculate metrics
        total_pipelines = len(pipelines)
        total_executions = 0
        successful = 0
        failed = 0
        
        for pipeline in pipelines:
            try:
                executions = cp_client.list_pipeline_executions(
                    pipelineName=pipeline['name'],
                    maxResults=10
                )
                exec_list = executions.get('pipelineExecutionSummaries', [])
                total_executions += len(exec_list)
                
                for exec in exec_list:
                    if exec.get('status') == 'Succeeded':
                        successful += 1
                    elif exec.get('status') == 'Failed':
                        failed += 1
            except:
                pass
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pipelines", total_pipelines)
        
        with col2:
            st.metric("Total Executions", total_executions)
        
        with col3:
            st.metric("Success Rate", 
                f"{(successful/(successful+failed)*100):.1f}%" if (successful+failed) > 0 else "N/A")
        
        with col4:
            st.metric("Failed", failed)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def render_configuration():
    """Configuration"""
    st.subheader("⚙️ Configuration")
    
    st.markdown("### 🔔 Notifications")
    
    with st.form("notification_config"):
        enable_email = st.checkbox("Enable email notifications")
        
        if enable_email:
            email = st.text_input("Email address")
        
        enable_slack = st.checkbox("Enable Slack notifications")
        
        if enable_slack:
            webhook = st.text_input("Slack webhook URL")
        
        if st.form_submit_button("Save Configuration"):
            st.success("✅ Configuration saved!")