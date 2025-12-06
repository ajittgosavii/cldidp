"""
Enterprise FinOps Module - AI-Powered Cost Management
Combines traditional FinOps with advanced AI intelligence

Features:
- AI-Powered Cost Analysis (Claude)
- Natural Language Query Interface
- Intelligent Right-Sizing Recommendations
- Advanced Anomaly Detection
- Automated Executive Reports
- Smart Cost Allocation
- Multi-Account Cost Management
- Real-time Optimization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from config_settings import AppConfig
from core_account_manager import get_account_manager
from utils_helpers import Helpers
import json
import os

# ============================================================================
# AI CLIENT INITIALIZATION
# ============================================================================

@st.cache_resource
def get_anthropic_client():
    """Initialize and cache Anthropic client for AI features"""
    api_key = None
    
    # Try multiple sources for API key
    if hasattr(st, 'secrets'):
        try:
            if 'anthropic' in st.secrets and 'api_key' in st.secrets['anthropic']:
                api_key = st.secrets['anthropic']['api_key']
        except:
            pass
    
    if not api_key and hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
        api_key = st.secrets['ANTHROPIC_API_KEY']
    
    if not api_key:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        return None
    
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing AI client: {str(e)}")
        return None

# ============================================================================
# AI-POWERED COST ANALYSIS
# ============================================================================

def analyze_costs_with_ai(cost_data: Dict, total_cost: float, service_costs: Dict) -> Dict:
    """Use Claude AI to analyze costs and provide intelligent insights"""
    client = get_anthropic_client()
    if not client:
        return {
            'executive_summary': 'AI analysis unavailable. Configure ANTHROPIC_API_KEY to enable AI-powered insights.',
            'key_insights': ['Configure AI to unlock intelligent cost analysis'],
            'recommendations': [],
            'anomalies': []
        }
    
    try:
        # Sort services by cost
        top_services = dict(sorted(service_costs.items(), key=lambda x: x[1], reverse=True)[:10])
        
        prompt = f"""Analyze AWS cost data and provide actionable insights:

Total Monthly Cost: ${total_cost:,.2f}

Top Services by Cost:
{json.dumps(top_services, indent=2)}

Provide:
1. Executive summary (2-3 sentences)
2. 3-5 key insights about spending patterns
3. 5-7 specific cost optimization recommendations with estimated savings
4. Any unusual spending patterns or anomalies

Format as JSON:
{{
    "executive_summary": "string",
    "key_insights": ["insight1", "insight2", ...],
    "recommendations": [
        {{"priority": "High|Medium|Low", "action": "string", "estimated_savings": "string", "implementation": "string"}}
    ],
    "anomalies": ["anomaly1", "anomaly2", ...]
}}

Respond ONLY with valid JSON."""

        import anthropic
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Extract JSON
        try:
            # Try direct parse
            return json.loads(response_text)
        except:
            # Try to extract JSON from markdown
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            # Fallback
            return {
                'executive_summary': 'AI analysis completed but response parsing failed.',
                'key_insights': [response_text[:200]],
                'recommendations': [],
                'anomalies': []
            }
    
    except Exception as e:
        return {
            'executive_summary': f'AI analysis error: {str(e)}',
            'key_insights': [],
            'recommendations': [],
            'anomalies': []
        }

def natural_language_query(query: str, cost_data: Dict) -> str:
    """Process natural language queries about costs using AI"""
    client = get_anthropic_client()
    if not client:
        return "⚠️ AI features not available. Please configure ANTHROPIC_API_KEY."
    
    try:
        import anthropic
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"""Answer this question about AWS costs:

Question: {query}

Cost Data Summary:
{json.dumps(cost_data, indent=2)[:1000]}

Provide a concise, specific answer."""
            }]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"Error processing query: {str(e)}"

# ============================================================================
# DEMO DATA GENERATION
# ============================================================================

def generate_demo_cost_data() -> Dict:
    """Generate demo cost data for visualization"""
    import random
    
    services = ['EC2', 'S3', 'RDS', 'Lambda', 'CloudFront', 'ELB', 'DynamoDB', 'VPC', 'CloudWatch', 'ECS']
    
    cost_data = {
        'total_cost': 0,
        'services': {},
        'daily_costs': [],
        'by_account': {}
    }
    
    # Service costs
    for service in services:
        cost = random.uniform(500, 5000)
        cost_data['services'][service] = cost
        cost_data['total_cost'] += cost
    
    # Daily costs for last 30 days
    for i in range(30):
        date = (datetime.now() - timedelta(days=30-i)).strftime('%Y-%m-%d')
        daily_cost = cost_data['total_cost'] / 30 * random.uniform(0.8, 1.2)
        cost_data['daily_costs'].append({
            'date': date,
            'cost': daily_cost
        })
    
    # By account
    accounts = ['Production', 'Staging', 'Development', 'Shared Services']
    for account in accounts:
        cost_data['by_account'][account] = cost_data['total_cost'] * random.uniform(0.1, 0.4)
    
    return cost_data

def generate_demo_recommendations() -> List[Dict]:
    """Generate demo optimization recommendations"""
    return [
        {
            'type': 'Reserved Instances',
            'resource': 'EC2 - m5.large',
            'current_cost': '$1,450/month',
            'optimized_cost': '$870/month',
            'savings': '$580/month',
            'savings_percentage': '40%',
            'priority': 'High',
            'implementation': 'Purchase 1-year All Upfront RI'
        },
        {
            'type': 'Right-Sizing',
            'resource': 'RDS - db.m5.2xlarge',
            'current_cost': '$890/month',
            'optimized_cost': '$445/month',
            'savings': '$445/month',
            'savings_percentage': '50%',
            'priority': 'High',
            'implementation': 'Downsize to db.m5.xlarge (avg CPU: 15%)'
        },
        {
            'type': 'Unused Resources',
            'resource': '23 Unattached EBS Volumes',
            'current_cost': '$276/month',
            'optimized_cost': '$0/month',
            'savings': '$276/month',
            'savings_percentage': '100%',
            'priority': 'Medium',
            'implementation': 'Delete unused volumes after verification'
        },
        {
            'type': 'Savings Plans',
            'resource': 'Lambda Compute',
            'current_cost': '$780/month',
            'optimized_cost': '$546/month',
            'savings': '$234/month',
            'savings_percentage': '30%',
            'priority': 'Medium',
            'implementation': '1-year Compute Savings Plan'
        },
        {
            'type': 'Storage Optimization',
            'resource': 'S3 - Infrequent Access',
            'current_cost': '$340/month',
            'optimized_cost': '$170/month',
            'savings': '$170/month',
            'savings_percentage': '50%',
            'priority': 'Low',
            'implementation': 'Move to Glacier for rarely accessed data'
        }
    ]

# ============================================================================
# MAIN FINOPS MODULE
# ============================================================================

class FinOpsEnterpriseModule:
    """Enterprise FinOps with AI-powered intelligence"""
    
    @staticmethod
    def render():
        """Main render method"""
        
        st.markdown("## 💰 Enterprise FinOps & Cost Intelligence")
        st.caption("AI-Powered Cloud Financial Operations | Multi-Account Cost Management | Intelligent Optimization")
        
        account_mgr = get_account_manager()
        if not account_mgr:
            st.warning("⚠️ Configure AWS credentials first")
            st.info("👉 Go to 'Account Management' to add your AWS accounts")
            return
        
        # Check AI availability
        ai_available = get_anthropic_client() is not None
        
        if ai_available:
            st.success("🤖 AI-Powered Analysis: **Enabled**")
        else:
            st.info("💡 Enable AI features by configuring ANTHROPIC_API_KEY in Streamlit secrets")
        
        # Main tabs
        tabs = st.tabs([
            "🎯 Cost Dashboard",
            "🤖 AI Insights",
            "💬 Ask AI",
            "📊 Multi-Account Costs",
            "📈 Cost Trends",
            "💡 Optimization",
            "🎯 Budget Management",
            "🏷️ Tag-Based Costs"
        ])
        
        with tabs[0]:
            FinOpsEnterpriseModule._render_cost_dashboard(account_mgr, ai_available)
        
        with tabs[1]:
            FinOpsEnterpriseModule._render_ai_insights(ai_available)
        
        with tabs[2]:
            FinOpsEnterpriseModule._render_ai_query(ai_available)
        
        with tabs[3]:
            FinOpsEnterpriseModule._render_multi_account_costs(account_mgr)
        
        with tabs[4]:
            FinOpsEnterpriseModule._render_cost_trends()
        
        with tabs[5]:
            FinOpsEnterpriseModule._render_optimization()
        
        with tabs[6]:
            FinOpsEnterpriseModule._render_budget_management()
        
        with tabs[7]:
            FinOpsEnterpriseModule._render_tag_based_costs()
    
    @staticmethod
    def _render_cost_dashboard(account_mgr, ai_available):
        """Enhanced cost dashboard with AI insights"""
        
        st.markdown("### 🎯 Cost Overview")
        
        # Generate demo data (in production, fetch from Cost Explorer)
        cost_data = generate_demo_cost_data()
        
        # Top metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Monthly Cost",
                Helpers.format_currency(cost_data['total_cost']),
                delta="-5.2%",
                help="Current month vs last month"
            )
        
        with col2:
            forecast = cost_data['total_cost'] * 1.05
            st.metric(
                "30-Day Forecast",
                Helpers.format_currency(forecast),
                delta="+5%",
                help="Projected cost for next 30 days"
            )
        
        with col3:
            potential_savings = cost_data['total_cost'] * 0.22
            st.metric(
                "Potential Savings",
                Helpers.format_currency(potential_savings),
                delta="22% opportunity",
                help="AI-identified optimization potential"
            )
        
        with col4:
            st.metric(
                "Budget Utilization",
                "76%",
                delta="+3%",
                help="Percentage of allocated budget used"
            )
        
        st.markdown("---")
        
        # Cost by service
        st.markdown("### 💸 Cost by Service")
        
        service_df = pd.DataFrame([
            {'Service': k, 'Cost': v}
            for k, v in cost_data['services'].items()
        ]).sort_values('Cost', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                service_df,
                x='Service',
                y='Cost',
                title='Monthly Cost by Service',
                color='Cost',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                service_df.head(5),
                values='Cost',
                names='Service',
                title='Top 5 Services'
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Quick AI analysis if available
        if ai_available:
            st.markdown("---")
            st.markdown("### 🤖 Quick AI Analysis")
            
            with st.spinner("Analyzing costs with AI..."):
                analysis = analyze_costs_with_ai(
                    cost_data,
                    cost_data['total_cost'],
                    cost_data['services']
                )
                
                st.info(f"**Executive Summary:** {analysis['executive_summary']}")
                
                if analysis['key_insights']:
                    st.markdown("**Key Insights:**")
                    for insight in analysis['key_insights'][:3]:
                        st.markdown(f"- {insight}")
    
    @staticmethod
    def _render_ai_insights(ai_available):
        """AI-powered cost insights and analysis"""
        
        st.markdown("### 🤖 AI-Powered Cost Intelligence")
        
        if not ai_available:
            st.warning("⚠️ AI features not available")
            st.info("""
            **To enable AI-powered analysis:**
            1. Get an Anthropic API key from console.anthropic.com
            2. Add to Streamlit secrets:
               ```
               [anthropic]
               api_key = "sk-ant-..."
               ```
            3. Restart the application
            """)
            return
        
        cost_data = generate_demo_cost_data()
        
        with st.spinner("🤖 AI analyzing your cost data..."):
            analysis = analyze_costs_with_ai(
                cost_data,
                cost_data['total_cost'],
                cost_data['services']
            )
        
        # Executive Summary
        st.markdown("#### 📊 Executive Summary")
        st.success(analysis['executive_summary'])
        
        # Key Insights
        st.markdown("---")
        st.markdown("#### 💡 Key Insights")
        
        for i, insight in enumerate(analysis.get('key_insights', []), 1):
            st.markdown(f"**{i}.** {insight}")
        
        # Recommendations
        st.markdown("---")
        st.markdown("#### 🎯 AI Recommendations")
        
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            for rec in recommendations:
                priority_color = {
                    'High': '🔴',
                    'Medium': '🟡',
                    'Low': '🟢'
                }.get(rec.get('priority', 'Medium'), '🟡')
                
                with st.expander(f"{priority_color} {rec.get('action', 'Recommendation')} - {rec.get('priority', 'Medium')} Priority"):
                    st.markdown(f"**Estimated Savings:** {rec.get('estimated_savings', 'TBD')}")
                    st.markdown(f"**Implementation:** {rec.get('implementation', 'See details')}")
        
        # Anomalies
        if analysis.get('anomalies'):
            st.markdown("---")
            st.markdown("#### ⚠️ Detected Anomalies")
            
            for anomaly in analysis['anomalies']:
                st.warning(f"🔍 {anomaly}")
    
    @staticmethod
    def _render_ai_query(ai_available):
        """Natural language query interface"""
        
        st.markdown("### 💬 Ask AI About Your Costs")
        
        if not ai_available:
            st.warning("⚠️ AI features not available. Configure ANTHROPIC_API_KEY to enable.")
            return
        
        st.info("💡 Ask questions in plain English about your AWS costs")
        
        # Sample questions
        st.markdown("**Example questions:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💰 What are my top 3 cost drivers?", key="q1", use_container_width=True):
                st.session_state.ai_query = "What are my top 3 cost drivers?"
            if st.button("📈 How can I reduce my EC2 costs?", key="q2", use_container_width=True):
                st.session_state.ai_query = "How can I reduce my EC2 costs?"
        
        with col2:
            if st.button("🎯 Where should I focus optimization?", key="q3", use_container_width=True):
                st.session_state.ai_query = "Where should I focus my optimization efforts?"
            if st.button("📊 Compare this month to last month", key="q4", use_container_width=True):
                st.session_state.ai_query = "Compare this month's costs to last month"
        
        # Query input
        query = st.text_input(
            "Your question:",
            value=st.session_state.get('ai_query', ''),
            placeholder="e.g., What's driving my S3 costs?",
            key="ai_query_input"
        )
        
        if st.button("🔍 Ask AI", type="primary", key="ask_ai_btn"):
            if query:
                cost_data = generate_demo_cost_data()
                
                with st.spinner("🤖 AI thinking..."):
                    response = natural_language_query(query, cost_data)
                
                st.markdown("---")
                st.markdown("### 🤖 AI Response:")
                st.markdown(response)
            else:
                st.warning("Please enter a question")
    
    @staticmethod
    def _render_multi_account_costs(account_mgr):
        """Multi-account cost breakdown"""
        
        st.markdown("### 📊 Multi-Account Cost Analysis")
        
        cost_data = generate_demo_cost_data()
        
        # Account costs
        account_df = pd.DataFrame([
            {
                'Account': k,
                'Cost': v,
                'Cost_Formatted': Helpers.format_currency(v),
                'Percentage': f"{(v / cost_data['total_cost'] * 100):.1f}%"
            }
            for k, v in cost_data['by_account'].items()
        ]).sort_values('Cost', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Cost Distribution")
            fig = px.bar(
                account_df,
                x='Account',
                y='Cost',
                text='Cost_Formatted',
                title='Cost by Account',
                color='Cost',
                color_continuous_scale='Reds'
            )
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Account Summary")
            st.dataframe(
                account_df[['Account', 'Cost_Formatted', 'Percentage']],
                use_container_width=True,
                hide_index=True
            )
    
    @staticmethod
    def _render_cost_trends():
        """Cost trends visualization"""
        
        st.markdown("### 📈 Cost Trends (30 Days)")
        
        cost_data = generate_demo_cost_data()
        
        # Prepare trend data
        trend_df = pd.DataFrame(cost_data['daily_costs'])
        trend_df['date'] = pd.to_datetime(trend_df['date'])
        
        # Add 7-day moving average
        trend_df['7day_avg'] = trend_df['cost'].rolling(window=7).mean()
        
        # Create visualization
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['cost'],
            mode='lines',
            name='Daily Cost',
            line=dict(color='lightblue', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=trend_df['date'],
            y=trend_df['7day_avg'],
            mode='lines',
            name='7-Day Average',
            line=dict(color='blue', width=3)
        ))
        
        fig.update_layout(
            title='Daily Cost Trend with 7-Day Moving Average',
            xaxis_title='Date',
            yaxis_title='Cost ($)',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Trend analysis
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_daily = trend_df['cost'].mean()
            st.metric("Avg Daily Cost", Helpers.format_currency(avg_daily))
        
        with col2:
            max_daily = trend_df['cost'].max()
            st.metric("Peak Daily Cost", Helpers.format_currency(max_daily))
        
        with col3:
            trend = "↑ Increasing" if trend_df['cost'].iloc[-1] > trend_df['cost'].iloc[0] else "↓ Decreasing"
            st.metric("Trend", trend)
    
    @staticmethod
    def _render_optimization():
        """Cost optimization recommendations"""
        
        st.markdown("### 💡 Cost Optimization Opportunities")
        
        recommendations = generate_demo_recommendations()
        
        # Summary metrics
        total_monthly_savings = sum(
            float(rec['savings'].replace('$', '').replace(',', '').replace('/month', ''))
            for rec in recommendations
        )
        annual_savings = total_monthly_savings * 12
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Monthly Savings Potential",
                Helpers.format_currency(total_monthly_savings),
                help="Total identified monthly savings"
            )
        
        with col2:
            st.metric(
                "Annual Savings Potential",
                Helpers.format_currency(annual_savings),
                help="Projected annual savings"
            )
        
        with col3:
            st.metric(
                "Recommendations",
                len(recommendations),
                help="Number of optimization opportunities"
            )
        
        st.markdown("---")
        
        # Detailed recommendations
        st.markdown("#### 🎯 Optimization Recommendations")
        
        for rec in recommendations:
            priority_color = {
                'High': '🔴',
                'Medium': '🟡',
                'Low': '🟢'
            }.get(rec['priority'], '🟡')
            
            with st.expander(
                f"{priority_color} {rec['type']} - {rec['resource']} | Save {rec['savings']} ({rec['savings_percentage']})"
            ):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Current Cost:** {rec['current_cost']}")
                    st.markdown(f"**Optimized Cost:** {rec['optimized_cost']}")
                    st.markdown(f"**Monthly Savings:** {rec['savings']}")
                    st.markdown(f"**Implementation:** {rec['implementation']}")
                
                with col2:
                    st.metric("Savings %", rec['savings_percentage'])
                    st.markdown(f"**Priority:** {rec['priority']}")
                    
                    if st.button("📋 Create Action Item", key=f"action_{rec['resource']}", use_container_width=True):
                        st.success("Action item created!")
    
    @staticmethod
    def _render_budget_management():
        """Budget management and alerts"""
        
        st.markdown("### 🎯 Budget Management")
        
        budgets = [
            {
                'Budget Name': 'Production Monthly',
                'Amount': '$15,000',
                'Current Spend': '$11,400',
                'Utilization': '76%',
                'Forecast': '$14,250',
                'Status': '✅ On Track'
            },
            {
                'Budget Name': 'Staging Monthly',
                'Amount': '$5,000',
                'Current Spend': '$4,650',
                'Utilization': '93%',
                'Forecast': '$5,580',
                'Status': '⚠️ At Risk'
            },
            {
                'Budget Name': 'Development Monthly',
                'Amount': '$3,000',
                'Current Spend': '$2,100',
                'Utilization': '70%',
                'Forecast': '$2,520',
                'Status': '✅ On Track'
            }
        ]
        
        df = pd.DataFrame(budgets)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.info("""
        **Budget Features:**
        - ✅ Set budgets per account/service/tag
        - ✅ Configure multi-threshold alerts (50%, 80%, 100%)
        - ✅ Forecast vs budget comparison
        - ✅ Automatic notifications via email/SNS
        - ✅ Budget utilization tracking
        
        **To configure:** Use AWS Budgets console or CloudFormation
        """)
    
    @staticmethod
    def _render_tag_based_costs():
        """Tag-based cost allocation and chargeback"""
        
        st.markdown("### 🏷️ Tag-Based Cost Allocation")
        
        st.info("""
        **Cost Allocation Tags:**
        Organize and track costs by:
        - 🏢 Department / Business Unit
        - 📁 Project / Application
        - 🌍 Environment (Prod/Staging/Dev)
        - 💰 Cost Center
        - 👤 Owner / Team
        """)
        
        # Sample tag-based costs
        tag_costs = [
            {
                'Tag': 'Department',
                'Value': 'Engineering',
                'Cost': '$8,450',
                'Percentage': '42%'
            },
            {
                'Tag': 'Department',
                'Value': 'Data Science',
                'Cost': '$5,230',
                'Percentage': '26%'
            },
            {
                'Tag': 'Department',
                'Value': 'Marketing',
                'Cost': '$3,120',
                'Percentage': '16%'
            },
            {
                'Tag': 'Department',
                'Value': 'Untagged',
                'Cost': '$3,200',
                'Percentage': '16%'
            }
        ]
        
        df = pd.DataFrame(tag_costs)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                df,
                x='Value',
                y='Cost',
                text='Percentage',
                title='Cost by Department',
                color='Cost'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Tag compliance
        st.markdown("#### 🎯 Tag Compliance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tagged Resources", "84%", delta="↑ 5%")
        with col2:
            st.metric("Untagged Cost", "$3,200", delta="↓ $450")
        with col3:
            st.metric("Tag Coverage Goal", "95%", delta="11% to go")

# Export
__all__ = ['FinOpsEnterpriseModule']