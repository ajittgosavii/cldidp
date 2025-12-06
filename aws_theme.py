"""
Light Sky Blue Theme Styling - Professional light blue UI
Light sky blue and white theme with excellent readability
"""

import streamlit as st

class AWSTheme:
    """Light Sky Blue themed styling for CloudIDP"""
    
    # Light Sky Blue Theme Colors
    SKY_BLUE = "#87CEEB"          # Primary - Light Sky Blue
    LIGHT_BG = "#F0F8FF"           # Alice Blue - Main background
    CARD_BG = "#E6F3FF"            # Light blue for cards
    SIDEBAR_BG = "#D4E9F7"         # Slightly darker for sidebar
    TEXT_DARK = "#1a1a1a"          # Dark text for readability
    TEXT_GRAY = "#4a4a4a"          # Gray text
    BORDER_BLUE = "#87CEEB"        # Border color
    HOVER_BLUE = "#6BB6E5"         # Darker blue for hover
    SUCCESS = "#28a745"            # Green for success
    WARNING = "#ffc107"            # Yellow for warning
    ERROR = "#dc3545"              # Red for error
    INFO_BLUE = "#0073BB"          # Info blue
    
    @staticmethod
    def apply_aws_theme():
        """Apply light sky blue theme to Streamlit"""
        
        st.markdown("""
        <style>
            /* ===== LIGHT SKY BLUE GLOBAL THEME ===== */
            
            /* Main app background */
            .stApp {
                background-color: #F0F8FF;
            }
            
            /* Main content area */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                background-color: #F0F8FF;
                max-width: 1400px;
            }
            
            /* ===== HEADER STYLING ===== */
            
            /* Main title */
            h1 {
                color: #1a1a1a !important;
                font-family: 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 700 !important;
                padding: 1rem 0;
                border-bottom: 3px solid #87CEEB;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #87CEEB 0%, #6BB6E5 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            h2 {
                color: #1a1a1a !important;
                font-family: 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 600 !important;
                margin-top: 1.5rem;
            }
            
            h3 {
                color: #1a1a1a !important;
                font-family: 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 500 !important;
            }
            
            /* ===== SIDEBAR ===== */
            
            /* Sidebar styling */
            [data-testid="stSidebar"] {
                background-color: #D4E9F7 !important;
                border-right: 3px solid #87CEEB;
            }
            
            [data-testid="stSidebar"] .block-container {
                padding-top: 1rem;
            }
            
            /* Sidebar text */
            [data-testid="stSidebar"] * {
                color: #1a1a1a !important;
            }
            
            /* Sidebar headers */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #1a1a1a !important;
                border-bottom: 2px solid #87CEEB;
                padding-bottom: 0.5rem;
            }
            
            /* Sidebar selectbox */
            [data-testid="stSidebar"] .stSelectbox,
            [data-testid="stSidebar"] .stRadio {
                background-color: #E6F3FF;
                border-radius: 4px;
                padding: 0.5rem;
            }
            
            /* ===== TABS ===== */
            
            /* Tab list container */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0px;
                background-color: #E6F3FF;
                border-bottom: 3px solid #87CEEB;
                padding: 0;
            }
            
            /* Individual tabs */
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: #FFFFFF;
                border: 1px solid #B0D4F1;
                border-bottom: none;
                color: #1a1a1a;
                font-weight: 600;
                font-size: 14px;
                padding: 0 1.5rem;
                margin: 0;
                border-radius: 4px 4px 0 0;
            }
            
            /* Active tab */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #87CEEB !important;
                color: #FFFFFF !important;
                border-bottom: 3px solid #87CEEB;
                font-weight: 700;
            }
            
            /* Tab hover effect */
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #B0E0F6;
                color: #1a1a1a;
            }
            
            /* Tab content */
            .stTabs [data-baseweb="tab-panel"] {
                background-color: #FFFFFF;
                padding: 1.5rem;
                border: 1px solid #B0D4F1;
                border-top: none;
                border-radius: 0 0 4px 4px;
            }
            
            /* ===== BUTTONS ===== */
            
            /* Primary button */
            .stButton > button {
                background-color: #87CEEB !important;
                color: #1a1a1a !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.6rem 1.8rem !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                transition: all 0.3s ease !important;
                font-family: 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                box-shadow: 0 2px 4px rgba(135, 206, 235, 0.3) !important;
            }
            
            .stButton > button:hover {
                background-color: #6BB6E5 !important;
                box-shadow: 0 4px 8px rgba(107, 182, 229, 0.4) !important;
                transform: translateY(-2px);
            }
            
            .stButton > button:active {
                transform: translateY(0);
                box-shadow: 0 2px 4px rgba(135, 206, 235, 0.3) !important;
            }
            
            /* ===== METRICS/CARDS ===== */
            
            /* Metric container */
            [data-testid="stMetric"] {
                background: linear-gradient(135deg, #FFFFFF 0%, #E6F3FF 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 2px solid #87CEEB;
                box-shadow: 0 4px 8px rgba(135, 206, 235, 0.2);
            }
            
            /* Metric label */
            [data-testid="stMetricLabel"] {
                color: #1a1a1a !important;
                font-weight: 600 !important;
                font-size: 14px !important;
            }
            
            /* Metric value */
            [data-testid="stMetricValue"] {
                color: #1a1a1a !important;
                font-weight: 700 !important;
                font-size: 32px !important;
            }
            
            /* Metric delta */
            [data-testid="stMetricDelta"] {
                color: #28a745 !important;
            }
            
            /* ===== DATAFRAMES/TABLES ===== */
            
            /* DataFrame styling */
            .dataframe {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #87CEEB !important;
                border-radius: 8px !important;
            }
            
            .dataframe thead tr th {
                background: linear-gradient(135deg, #87CEEB 0%, #6BB6E5 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                padding: 12px !important;
                border: none !important;
            }
            
            .dataframe tbody tr {
                background-color: #FFFFFF !important;
                border-bottom: 1px solid #E6F3FF !important;
            }
            
            .dataframe tbody tr:hover {
                background-color: #F0F8FF !important;
            }
            
            .dataframe tbody tr td {
                color: #1a1a1a !important;
                padding: 10px !important;
            }
            
            /* Alternating row colors */
            .dataframe tbody tr:nth-child(even) {
                background-color: #F8FCFF !important;
            }
            
            /* ===== INPUT FIELDS ===== */
            
            /* Text inputs */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stNumberInput > div > div > input {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 8px !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stNumberInput > div > div > input:focus {
                border-color: #87CEEB !important;
                box-shadow: 0 0 0 3px rgba(135, 206, 235, 0.2) !important;
            }
            
            /* Select boxes */
            .stSelectbox > div > div {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 8px !important;
            }
            
            /* Multiselect */
            .stMultiSelect > div > div {
                background-color: #FFFFFF !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 8px !important;
            }
            
            /* ===== ALERTS/MESSAGES ===== */
            
            /* Success message */
            .stSuccess {
                background-color: #d4edda !important;
                border-left: 4px solid #28a745 !important;
                color: #155724 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* Info message */
            .stInfo {
                background-color: #d1ecf1 !important;
                border-left: 4px solid #0073BB !important;
                color: #0c5460 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* Warning message */
            .stWarning {
                background-color: #fff3cd !important;
                border-left: 4px solid #ffc107 !important;
                color: #856404 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* Error message */
            .stError {
                background-color: #f8d7da !important;
                border-left: 4px solid #dc3545 !important;
                color: #721c24 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* ===== EXPANDERS ===== */
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #E6F3FF !important;
                color: #1a1a1a !important;
                border: 2px solid #87CEEB !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
            }
            
            .streamlit-expanderHeader:hover {
                background-color: #D4E9F7 !important;
            }
            
            .streamlit-expanderContent {
                background-color: #FFFFFF !important;
                border: 2px solid #B0D4F1 !important;
                border-top: none !important;
                color: #1a1a1a !important;
                border-radius: 0 0 8px 8px !important;
            }
            
            /* ===== PROGRESS BARS ===== */
            
            .stProgress > div > div > div {
                background: linear-gradient(90deg, #87CEEB 0%, #6BB6E5 100%) !important;
            }
            
            /* ===== CHARTS ===== */
            
            /* Chart backgrounds */
            [data-testid="stPlotlyChart"] {
                background-color: #FFFFFF !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
            
            /* ===== DIVIDERS ===== */
            
            hr {
                border-color: #87CEEB !important;
                opacity: 0.6 !important;
            }
            
            /* ===== CUSTOM COMPONENTS ===== */
            
            /* Sky Blue Header Banner */
            .aws-header {
                background: linear-gradient(135deg, #87CEEB 0%, #6BB6E5 100%);
                padding: 2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 12px rgba(135, 206, 235, 0.3);
                border: 2px solid #87CEEB;
            }
            
            .aws-header h1 {
                color: #FFFFFF !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
                -webkit-text-fill-color: #FFFFFF !important;
            }
            
            .aws-header p {
                color: #FFFFFF !important;
                margin: 0.5rem 0 0 0 !important;
                font-size: 1.1rem !important;
            }
            
            /* Sky Blue Service Card */
            .aws-service-card {
                background: linear-gradient(135deg, #FFFFFF 0%, #F0F8FF 100%);
                border: 2px solid #87CEEB;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(135, 206, 235, 0.2);
                transition: all 0.3s ease;
            }
            
            .aws-service-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 8px 16px rgba(107, 182, 229, 0.3);
                border-color: #6BB6E5;
            }
            
            /* Status Badge */
            .aws-badge {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.875rem;
                margin: 0.25rem;
            }
            
            .aws-badge-success {
                background-color: #28a745;
                color: #FFFFFF;
            }
            
            .aws-badge-warning {
                background-color: #ffc107;
                color: #1a1a1a;
            }
            
            .aws-badge-error {
                background-color: #dc3545;
                color: #FFFFFF;
            }
            
            .aws-badge-info {
                background-color: #87CEEB;
                color: #FFFFFF;
            }
            
            /* Stats Row */
            .aws-stats-row {
                display: flex;
                gap: 1rem;
                margin: 1rem 0;
            }
            
            /* ===== SCROLLBAR ===== */
            
            ::-webkit-scrollbar {
                width: 12px;
                height: 12px;
            }
            
            ::-webkit-scrollbar-track {
                background: #E6F3FF;
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #87CEEB;
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #6BB6E5;
            }
            
            /* ===== RADIO BUTTONS ===== */
            
            .stRadio > div {
                background-color: #F0F8FF;
                padding: 0.5rem;
                border-radius: 8px;
            }
            
            .stRadio label {
                color: #1a1a1a !important;
            }
            
            /* ===== CHECKBOXES ===== */
            
            .stCheckbox {
                color: #1a1a1a !important;
            }
            
            /* ===== TEXT ===== */
            
            p, span, label, li {
                color: #1a1a1a !important;
            }
            
            .stMarkdown {
                color: #1a1a1a !important;
            }
            
            /* Caption text */
            .stCaption {
                color: #4a4a4a !important;
            }
            
            /* Code blocks */
            code {
                background-color: #E6F3FF !important;
                color: #1a1a1a !important;
                padding: 0.2rem 0.4rem !important;
                border-radius: 4px !important;
                border: 1px solid #B0D4F1 !important;
            }
            
            /* ===== CHAT MESSAGES ===== */
            
            .stChatMessage {
                background-color: #FFFFFF !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 12px !important;
            }
            
            /* ===== FOOTER ===== */
            
            footer {
                background-color: #E6F3FF !important;
                border-top: 3px solid #87CEEB !important;
            }
            
            footer p {
                color: #1a1a1a !important;
            }
            
            /* ===== FILE UPLOADER ===== */
            
            [data-testid="stFileUploader"] {
                background-color: #FFFFFF !important;
                border: 2px dashed #87CEEB !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
            
            /* ===== DOWNLOAD BUTTON ===== */
            
            .stDownloadButton > button {
                background-color: #87CEEB !important;
                color: #1a1a1a !important;
                border: none !important;
                border-radius: 8px !important;
            }
            
            .stDownloadButton > button:hover {
                background-color: #6BB6E5 !important;
            }
            
            /* ===== SPINNER ===== */
            
            .stSpinner > div {
                border-top-color: #87CEEB !important;
            }
            
            /* ===== SLIDER ===== */
            
            .stSlider [data-baseweb="slider"] {
                background-color: #E6F3FF !important;
            }
            
            .stSlider [data-baseweb="slider"] [role="slider"] {
                background-color: #87CEEB !important;
            }
            
            /* ===== DATE INPUT ===== */
            
            .stDateInput > div > div > input {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 8px !important;
            }
            
            /* ===== TIME INPUT ===== */
            
            .stTimeInput > div > div > input {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #B0D4F1 !important;
                border-radius: 8px !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_header(title: str, subtitle: str = None):
        """Create sky blue styled header banner"""
        subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
        
        st.markdown(f"""
        <div class="aws-header">
            <h1>☁️ {title}</h1>
            {subtitle_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_service_card(title: str, content: str, icon: str = "📦"):
        """Create sky blue styled service card"""
        st.markdown(f"""
        <div class="aws-service-card">
            <h3>{icon} {title}</h3>
            <p style="color: #1a1a1a !important;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_badge(text: str, badge_type: str = "info"):
        """Create sky blue styled status badge"""
        return f'<span class="aws-badge aws-badge-{badge_type}">{text}</span>'
    
    @staticmethod
    def aws_metric_card(label: str, value: str, delta: str = None, icon: str = "📊"):
        """Create sky blue styled metric card with icon"""
        delta_html = f'<div style="color: #28a745; margin-top: 0.5rem;">{delta}</div>' if delta else ''
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #E6F3FF 100%); 
                    padding: 1.5rem; border-radius: 12px; 
                    border: 2px solid #87CEEB; box-shadow: 0 4px 8px rgba(135, 206, 235, 0.2);">
            <div style="color: #1a1a1a; font-weight: 600; font-size: 14px; margin-bottom: 0.5rem;">
                {icon} {label}
            </div>
            <div style="color: #1a1a1a; font-weight: 700; font-size: 32px;">
                {value}
            </div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)