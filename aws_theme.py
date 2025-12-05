"""
AWS Theme Styling - Professional AWS-branded UI
Orange and dark theme matching AWS Console design
"""

import streamlit as st

class AWSTheme:
    """AWS-themed styling for CloudIDP"""
    
    # AWS Brand Colors
    AWS_ORANGE = "#FF9900"
    AWS_DARK = "#232F3E"
    AWS_DARK_GRAY = "#161E2D"
    AWS_LIGHT_GRAY = "#F2F3F4"
    AWS_GRAY = "#545B64"
    AWS_WHITE = "#FFFFFF"
    AWS_BLUE = "#0073BB"
    AWS_SUCCESS = "#00A86B"
    AWS_WARNING = "#FFB81C"
    AWS_ERROR = "#D13212"
    
    @staticmethod
    def apply_aws_theme():
        """Apply AWS console-style theme to Streamlit"""
        
        st.markdown("""
        <style>
            /* ===== AWS GLOBAL THEME ===== */
            
            /* Main app background */
            .stApp {
                background-color: #232F3E;
            }
            
            /* Main content area */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                background-color: #232F3E;
                max-width: 1400px;
            }
            
            /* ===== AWS HEADER STYLING ===== */
            
            /* Main title */
            h1 {
                color: #FF9900 !important;
                font-family: 'Amazon Ember', 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 700 !important;
                padding: 1rem 0;
                border-bottom: 3px solid #FF9900;
                margin-bottom: 1.5rem;
            }
            
            h2 {
                color: #FF9900 !important;
                font-family: 'Amazon Ember', 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 600 !important;
                margin-top: 1.5rem;
            }
            
            h3 {
                color: #FFFFFF !important;
                font-family: 'Amazon Ember', 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 500 !important;
            }
            
            /* ===== AWS SIDEBAR ===== */
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #161E2D !important;
                border-right: 2px solid #FF9900;
            }
            
            [data-testid="stSidebar"] .block-container {
                padding-top: 1rem;
            }
            
            /* Sidebar text */
            [data-testid="stSidebar"] * {
                color: #FFFFFF !important;
            }
            
            /* Sidebar headers */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #FF9900 !important;
                border-bottom: 1px solid #FF9900;
                padding-bottom: 0.5rem;
            }
            
            /* Sidebar selectbox */
            [data-testid="stSidebar"] .stSelectbox,
            [data-testid="stSidebar"] .stRadio {
                background-color: #232F3E;
                border-radius: 4px;
                padding: 0.5rem;
            }
            
            /* ===== AWS TABS ===== */
            
            /* Tab list container */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0px;
                background-color: #161E2D;
                border-bottom: 2px solid #FF9900;
                padding: 0;
            }
            
            /* Individual tabs */
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: #232F3E;
                border: 1px solid #444444;
                border-bottom: none;
                color: #FFFFFF;
                font-weight: 600;
                font-size: 14px;
                padding: 0 1.5rem;
                margin: 0;
                border-radius: 4px 4px 0 0;
            }
            
            /* Active tab */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #FF9900 !important;
                color: #232F3E !important;
                border-bottom: 2px solid #FF9900;
            }
            
            /* Tab hover effect */
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #FF9900;
                color: #232F3E;
            }
            
            /* Tab content */
            .stTabs [data-baseweb="tab-panel"] {
                background-color: #232F3E;
                padding: 1.5rem;
                border: 1px solid #444444;
                border-top: none;
                border-radius: 0 0 4px 4px;
            }
            
            /* ===== AWS BUTTONS ===== */
            
            /* Primary button */
            .stButton > button {
                background-color: #FF9900 !important;
                color: #232F3E !important;
                border: none !important;
                border-radius: 4px !important;
                padding: 0.5rem 1.5rem !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                transition: all 0.3s ease !important;
                font-family: 'Amazon Ember', 'Helvetica Neue', Roboto, Arial, sans-serif !important;
            }
            
            .stButton > button:hover {
                background-color: #EC7211 !important;
                box-shadow: 0 4px 8px rgba(255, 153, 0, 0.3) !important;
                transform: translateY(-1px);
            }
            
            .stButton > button:active {
                transform: translateY(0);
            }
            
            /* ===== AWS METRICS/CARDS ===== */
            
            /* Metric container */
            [data-testid="stMetric"] {
                background-color: #161E2D;
                padding: 1.5rem;
                border-radius: 8px;
                border: 2px solid #FF9900;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            
            /* Metric label */
            [data-testid="stMetricLabel"] {
                color: #FF9900 !important;
                font-weight: 600 !important;
                font-size: 14px !important;
            }
            
            /* Metric value */
            [data-testid="stMetricValue"] {
                color: #FFFFFF !important;
                font-weight: 700 !important;
                font-size: 32px !important;
            }
            
            /* Metric delta */
            [data-testid="stMetricDelta"] {
                color: #00A86B !important;
            }
            
            /* ===== AWS DATAFRAMES/TABLES ===== */
            
            /* DataFrame styling */
            .dataframe {
                background-color: #161E2D !important;
                color: #FFFFFF !important;
                border: 1px solid #FF9900 !important;
            }
            
            .dataframe thead tr th {
                background-color: #FF9900 !important;
                color: #232F3E !important;
                font-weight: 700 !important;
                padding: 12px !important;
                border: none !important;
            }
            
            .dataframe tbody tr {
                background-color: #232F3E !important;
                border-bottom: 1px solid #444444 !important;
            }
            
            .dataframe tbody tr:hover {
                background-color: #2C3E50 !important;
            }
            
            .dataframe tbody tr td {
                color: #FFFFFF !important;
                padding: 10px !important;
            }
            
            /* ===== AWS INPUT FIELDS ===== */
            
            /* Text inputs */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stNumberInput > div > div > input {
                background-color: #161E2D !important;
                color: #FFFFFF !important;
                border: 2px solid #545B64 !important;
                border-radius: 4px !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stNumberInput > div > div > input:focus {
                border-color: #FF9900 !important;
                box-shadow: 0 0 0 2px rgba(255, 153, 0, 0.2) !important;
            }
            
            /* Select boxes */
            .stSelectbox > div > div {
                background-color: #161E2D !important;
                color: #FFFFFF !important;
                border: 2px solid #545B64 !important;
                border-radius: 4px !important;
            }
            
            /* Multiselect */
            .stMultiSelect > div > div {
                background-color: #161E2D !important;
                border: 2px solid #545B64 !important;
            }
            
            /* ===== AWS ALERTS/MESSAGES ===== */
            
            /* Success message */
            .stSuccess {
                background-color: rgba(0, 168, 107, 0.1) !important;
                border-left: 4px solid #00A86B !important;
                color: #FFFFFF !important;
                padding: 1rem !important;
                border-radius: 4px !important;
            }
            
            /* Info message */
            .stInfo {
                background-color: rgba(0, 115, 187, 0.1) !important;
                border-left: 4px solid #0073BB !important;
                color: #FFFFFF !important;
                padding: 1rem !important;
                border-radius: 4px !important;
            }
            
            /* Warning message */
            .stWarning {
                background-color: rgba(255, 184, 28, 0.1) !important;
                border-left: 4px solid #FFB81C !important;
                color: #FFFFFF !important;
                padding: 1rem !important;
                border-radius: 4px !important;
            }
            
            /* Error message */
            .stError {
                background-color: rgba(209, 50, 18, 0.1) !important;
                border-left: 4px solid #D13212 !important;
                color: #FFFFFF !important;
                padding: 1rem !important;
                border-radius: 4px !important;
            }
            
            /* ===== AWS EXPANDERS ===== */
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #161E2D !important;
                color: #FF9900 !important;
                border: 1px solid #FF9900 !important;
                border-radius: 4px !important;
                font-weight: 600 !important;
            }
            
            .streamlit-expanderHeader:hover {
                background-color: #232F3E !important;
            }
            
            .streamlit-expanderContent {
                background-color: #232F3E !important;
                border: 1px solid #444444 !important;
                border-top: none !important;
                color: #FFFFFF !important;
            }
            
            /* ===== AWS PROGRESS BARS ===== */
            
            .stProgress > div > div > div {
                background-color: #FF9900 !important;
            }
            
            /* ===== AWS CHARTS ===== */
            
            /* Chart backgrounds */
            [data-testid="stPlotlyChart"] {
                background-color: #161E2D !important;
                border: 1px solid #444444 !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }
            
            /* ===== AWS DIVIDERS ===== */
            
            hr {
                border-color: #FF9900 !important;
                opacity: 0.5 !important;
            }
            
            /* ===== CUSTOM AWS COMPONENTS ===== */
            
            /* AWS Header Banner */
            .aws-header {
                background: linear-gradient(135deg, #232F3E 0%, #FF9900 100%);
                padding: 2rem;
                border-radius: 8px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                border: 1px solid #FF9900;
            }
            
            .aws-header h1 {
                color: #FFFFFF !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
            }
            
            .aws-header p {
                color: #F2F3F4 !important;
                margin: 0.5rem 0 0 0 !important;
                font-size: 1.1rem !important;
            }
            
            /* AWS Service Card */
            .aws-service-card {
                background-color: #161E2D;
                border: 2px solid #FF9900;
                border-radius: 8px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
            }
            
            .aws-service-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 12px rgba(255, 153, 0, 0.3);
                border-color: #EC7211;
            }
            
            /* AWS Status Badge */
            .aws-badge {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.875rem;
                margin: 0.25rem;
            }
            
            .aws-badge-success {
                background-color: #00A86B;
                color: #FFFFFF;
            }
            
            .aws-badge-warning {
                background-color: #FFB81C;
                color: #232F3E;
            }
            
            .aws-badge-error {
                background-color: #D13212;
                color: #FFFFFF;
            }
            
            .aws-badge-info {
                background-color: #0073BB;
                color: #FFFFFF;
            }
            
            /* AWS Stats Row */
            .aws-stats-row {
                display: flex;
                gap: 1rem;
                margin: 1rem 0;
            }
            
            /* ===== SCROLLBAR ===== */
            
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #161E2D;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #FF9900;
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #EC7211;
            }
            
            /* ===== RADIO BUTTONS ===== */
            
            .stRadio > div {
                background-color: #161E2D;
                padding: 0.5rem;
                border-radius: 4px;
            }
            
            .stRadio label {
                color: #FFFFFF !important;
            }
            
            /* ===== CHECKBOXES ===== */
            
            .stCheckbox {
                color: #FFFFFF !important;
            }
            
            /* ===== TEXT ===== */
            
            p, span, label, li {
                color: #FFFFFF !important;
            }
            
            .stMarkdown {
                color: #FFFFFF !important;
            }
            
            /* Caption text */
            .stCaption {
                color: #F2F3F4 !important;
            }
            
            /* ===== CHAT MESSAGES ===== */
            
            .stChatMessage {
                background-color: #161E2D !important;
                border: 1px solid #444444 !important;
                border-radius: 8px !important;
            }
            
            /* ===== FOOTER ===== */
            
            footer {
                background-color: #161E2D !important;
                border-top: 2px solid #FF9900 !important;
            }
            
            footer p {
                color: #F2F3F4 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_header(title: str, subtitle: str = None):
        """Create AWS-styled header banner"""
        subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
        
        st.markdown(f"""
        <div class="aws-header">
            <h1>☁️ {title}</h1>
            {subtitle_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_service_card(title: str, content: str, icon: str = "📦"):
        """Create AWS-styled service card"""
        st.markdown(f"""
        <div class="aws-service-card">
            <h3>{icon} {title}</h3>
            <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_badge(text: str, badge_type: str = "info"):
        """Create AWS-styled status badge"""
        return f'<span class="aws-badge aws-badge-{badge_type}">{text}</span>'
    
    @staticmethod
    def aws_metric_card(label: str, value: str, delta: str = None, icon: str = "📊"):
        """Create AWS-styled metric card with icon"""
        delta_html = f'<div style="color: #00A86B; margin-top: 0.5rem;">{delta}</div>' if delta else ''
        
        st.markdown(f"""
        <div style="background-color: #161E2D; padding: 1.5rem; border-radius: 8px; 
                    border: 2px solid #FF9900; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">
            <div style="color: #FF9900; font-weight: 600; font-size: 14px; margin-bottom: 0.5rem;">
                {icon} {label}
            </div>
            <div style="color: #FFFFFF; font-weight: 700; font-size: 32px;">
                {value}
            </div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
