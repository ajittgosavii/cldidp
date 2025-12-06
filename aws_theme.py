"""
Ultra-Light Pastel Sky Blue Theme - Soft, Airy, Professional
Very light pastel blue with excellent readability
"""

import streamlit as st

class AWSTheme:
    """Ultra-light pastel sky blue themed styling for CloudIDP"""
    
    # Ultra-Light Pastel Sky Blue Theme Colors
    PASTEL_SKY_BLUE = "#B3E5FC"    # Very light sky blue (primary)
    SOFT_BLUE = "#81D4FA"          # Soft blue (hover/active)
    LIGHTEST_BG = "#FAFCFF"        # Almost white with hint of blue
    CARD_BG = "#F5FAFF"            # Very light blue for cards
    SIDEBAR_BG = "#EBF5FB"         # Light blue sidebar
    TEXT_DARK = "#1a1a1a"          # Dark text for readability
    TEXT_GRAY = "#5a5a5a"          # Gray text
    BORDER_LIGHT = "#B3E5FC"       # Light blue border
    SUCCESS = "#4caf50"            # Green
    WARNING = "#ff9800"            # Orange
    ERROR = "#f44336"              # Red
    INFO_BLUE = "#29b6f6"          # Light info blue
    
    @staticmethod
    def apply_aws_theme():
        """Apply ultra-light pastel sky blue theme to Streamlit"""
        
        st.markdown("""
        <style>
            /* ===== ULTRA-LIGHT PASTEL SKY BLUE THEME ===== */
            
            /* Main app background - almost white */
            .stApp {
                background-color: #FAFCFF;
            }
            
            /* Main content area */
            .main .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
                background-color: #FAFCFF;
                max-width: 1400px;
            }
            
            /* ===== HEADER STYLING ===== */
            
            /* Main title */
            h1 {
                color: #1a1a1a !important;
                font-family: 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                font-weight: 700 !important;
                padding: 1rem 0;
                border-bottom: 3px solid #B3E5FC;
                margin-bottom: 1.5rem;
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
            
            /* Sidebar styling - very light blue */
            [data-testid="stSidebar"] {
                background-color: #EBF5FB !important;
                border-right: 3px solid #B3E5FC;
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
                border-bottom: 2px solid #B3E5FC;
                padding-bottom: 0.5rem;
            }
            
            /* Sidebar selectbox */
            [data-testid="stSidebar"] .stSelectbox,
            [data-testid="stSidebar"] .stRadio {
                background-color: #F5FAFF;
                border-radius: 8px;
                padding: 0.5rem;
            }
            
            /* ===== TABS ===== */
            
            /* Tab list container */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0px;
                background-color: #F5FAFF;
                border-bottom: 3px solid #B3E5FC;
                padding: 0;
            }
            
            /* Individual tabs */
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                background-color: #FFFFFF;
                border: 1px solid #D4E9F7;
                border-bottom: none;
                color: #1a1a1a;
                font-weight: 600;
                font-size: 14px;
                padding: 0 1.5rem;
                margin: 0;
                border-radius: 8px 8px 0 0;
            }
            
            /* Active tab - pastel blue */
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background: linear-gradient(180deg, #B3E5FC 0%, #81D4FA 100%) !important;
                color: #FFFFFF !important;
                border-bottom: 3px solid #81D4FA;
                font-weight: 700;
            }
            
            /* Tab hover effect */
            .stTabs [data-baseweb="tab"]:hover {
                background-color: #E1F5FE;
                color: #1a1a1a;
            }
            
            /* Tab content */
            .stTabs [data-baseweb="tab-panel"] {
                background-color: #FFFFFF;
                padding: 1.5rem;
                border: 1px solid #D4E9F7;
                border-top: none;
                border-radius: 0 0 8px 8px;
            }
            
            /* ===== BUTTONS ===== */
            
            /* Primary button - pastel blue */
            .stButton > button {
                background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.7rem 2rem !important;
                font-weight: 600 !important;
                font-size: 14px !important;
                transition: all 0.3s ease !important;
                font-family: 'Helvetica Neue', Roboto, Arial, sans-serif !important;
                box-shadow: 0 2px 8px rgba(129, 212, 250, 0.3) !important;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
            }
            
            .stButton > button:hover {
                background: linear-gradient(135deg, #81D4FA 0%, #4FC3F7 100%) !important;
                box-shadow: 0 4px 12px rgba(79, 195, 247, 0.4) !important;
                transform: translateY(-2px);
            }
            
            .stButton > button:active {
                transform: translateY(0);
                box-shadow: 0 2px 6px rgba(129, 212, 250, 0.3) !important;
            }
            
            /* ===== METRICS/CARDS ===== */
            
            /* Metric container */
            [data-testid="stMetric"] {
                background: linear-gradient(135deg, #FFFFFF 0%, #F5FAFF 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 2px solid #B3E5FC;
                box-shadow: 0 2px 8px rgba(179, 229, 252, 0.2);
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
                color: #4caf50 !important;
            }
            
            /* ===== DATAFRAMES/TABLES ===== */
            
            /* DataFrame styling */
            .dataframe {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #B3E5FC !important;
                border-radius: 8px !important;
            }
            
            .dataframe thead tr th {
                background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%) !important;
                color: #FFFFFF !important;
                font-weight: 700 !important;
                padding: 12px !important;
                border: none !important;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
            }
            
            .dataframe tbody tr {
                background-color: #FFFFFF !important;
                border-bottom: 1px solid #F5FAFF !important;
            }
            
            .dataframe tbody tr:hover {
                background-color: #F5FAFF !important;
            }
            
            .dataframe tbody tr td {
                color: #1a1a1a !important;
                padding: 10px !important;
            }
            
            /* Alternating row colors */
            .dataframe tbody tr:nth-child(even) {
                background-color: #FAFCFF !important;
            }
            
            /* ===== INPUT FIELDS ===== */
            
            /* Text inputs */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stNumberInput > div > div > input {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 8px !important;
            }
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus,
            .stNumberInput > div > div > input:focus {
                border-color: #B3E5FC !important;
                box-shadow: 0 0 0 3px rgba(179, 229, 252, 0.2) !important;
            }
            
            /* Select boxes */
            .stSelectbox > div > div {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 8px !important;
            }
            
            /* Multiselect */
            .stMultiSelect > div > div {
                background-color: #FFFFFF !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 8px !important;
            }
            
            /* ===== ALERTS/MESSAGES ===== */
            
            /* Success message */
            .stSuccess {
                background-color: #e8f5e9 !important;
                border-left: 4px solid #4caf50 !important;
                color: #2e7d32 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* Info message */
            .stInfo {
                background-color: #e1f5fe !important;
                border-left: 4px solid #29b6f6 !important;
                color: #01579b !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* Warning message */
            .stWarning {
                background-color: #fff3e0 !important;
                border-left: 4px solid #ff9800 !important;
                color: #e65100 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* Error message */
            .stError {
                background-color: #ffebee !important;
                border-left: 4px solid #f44336 !important;
                color: #c62828 !important;
                padding: 1rem !important;
                border-radius: 8px !important;
            }
            
            /* ===== EXPANDERS ===== */
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #F5FAFF !important;
                color: #1a1a1a !important;
                border: 2px solid #B3E5FC !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
            }
            
            .streamlit-expanderHeader:hover {
                background-color: #E1F5FE !important;
            }
            
            .streamlit-expanderContent {
                background-color: #FFFFFF !important;
                border: 2px solid #D4E9F7 !important;
                border-top: none !important;
                color: #1a1a1a !important;
                border-radius: 0 0 8px 8px !important;
            }
            
            /* ===== PROGRESS BARS ===== */
            
            .stProgress > div > div > div {
                background: linear-gradient(90deg, #B3E5FC 0%, #81D4FA 100%) !important;
            }
            
            /* ===== CHARTS ===== */
            
            /* Chart backgrounds */
            [data-testid="stPlotlyChart"] {
                background-color: #FFFFFF !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
            
            /* ===== DIVIDERS ===== */
            
            hr {
                border-color: #B3E5FC !important;
                opacity: 0.6 !important;
            }
            
            /* ===== CUSTOM COMPONENTS ===== */
            
            /* Pastel Blue Header Banner */
            .aws-header {
                background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%);
                padding: 2rem;
                border-radius: 12px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 12px rgba(179, 229, 252, 0.3);
                border: 2px solid #B3E5FC;
            }
            
            .aws-header h1 {
                color: #FFFFFF !important;
                margin: 0 !important;
                padding: 0 !important;
                border: none !important;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
            }
            
            .aws-header p {
                color: #FFFFFF !important;
                margin: 0.5rem 0 0 0 !important;
                font-size: 1.1rem !important;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Pastel Service Card */
            .aws-service-card {
                background: linear-gradient(135deg, #FFFFFF 0%, #F5FAFF 100%);
                border: 2px solid #B3E5FC;
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
                box-shadow: 0 2px 8px rgba(179, 229, 252, 0.2);
                transition: all 0.3s ease;
            }
            
            .aws-service-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 6px 16px rgba(129, 212, 250, 0.3);
                border-color: #81D4FA;
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
                background-color: #4caf50;
                color: #FFFFFF;
            }
            
            .aws-badge-warning {
                background-color: #ff9800;
                color: #FFFFFF;
            }
            
            .aws-badge-error {
                background-color: #f44336;
                color: #FFFFFF;
            }
            
            .aws-badge-info {
                background-color: #29b6f6;
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
                background: #F5FAFF;
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #B3E5FC;
                border-radius: 6px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #81D4FA;
            }
            
            /* ===== RADIO BUTTONS ===== */
            
            .stRadio > div {
                background-color: #F5FAFF;
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
                color: #5a5a5a !important;
            }
            
            /* Code blocks */
            code {
                background-color: #F5FAFF !important;
                color: #1a1a1a !important;
                padding: 0.2rem 0.4rem !important;
                border-radius: 4px !important;
                border: 1px solid #D4E9F7 !important;
            }
            
            /* ===== CHAT MESSAGES ===== */
            
            .stChatMessage {
                background-color: #FFFFFF !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 12px !important;
            }
            
            /* ===== FOOTER ===== */
            
            footer {
                background-color: #F5FAFF !important;
                border-top: 3px solid #B3E5FC !important;
            }
            
            footer p {
                color: #1a1a1a !important;
            }
            
            /* ===== FILE UPLOADER ===== */
            
            [data-testid="stFileUploader"] {
                background-color: #FFFFFF !important;
                border: 2px dashed #B3E5FC !important;
                border-radius: 12px !important;
                padding: 1rem !important;
            }
            
            /* ===== DOWNLOAD BUTTON ===== */
            
            .stDownloadButton > button {
                background: linear-gradient(135deg, #B3E5FC 0%, #81D4FA 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 8px !important;
            }
            
            .stDownloadButton > button:hover {
                background: linear-gradient(135deg, #81D4FA 0%, #4FC3F7 100%) !important;
            }
            
            /* ===== SPINNER ===== */
            
            .stSpinner > div {
                border-top-color: #B3E5FC !important;
            }
            
            /* ===== SLIDER ===== */
            
            .stSlider [data-baseweb="slider"] {
                background-color: #F5FAFF !important;
            }
            
            .stSlider [data-baseweb="slider"] [role="slider"] {
                background-color: #B3E5FC !important;
            }
            
            /* ===== DATE INPUT ===== */
            
            .stDateInput > div > div > input {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 8px !important;
            }
            
            /* ===== TIME INPUT ===== */
            
            .stTimeInput > div > div > input {
                background-color: #FFFFFF !important;
                color: #1a1a1a !important;
                border: 2px solid #D4E9F7 !important;
                border-radius: 8px !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_header(title: str, subtitle: str = None):
        """Create pastel blue styled header banner"""
        subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
        
        st.markdown(f"""
        <div class="aws-header">
            <h1>☁️ {title}</h1>
            {subtitle_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_service_card(title: str, content: str, icon: str = "📦"):
        """Create pastel blue styled service card"""
        st.markdown(f"""
        <div class="aws-service-card">
            <h3>{icon} {title}</h3>
            <p style="color: #1a1a1a !important;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def aws_badge(text: str, badge_type: str = "info"):
        """Create pastel blue styled status badge"""
        return f'<span class="aws-badge aws-badge-{badge_type}">{text}</span>'
    
    @staticmethod
    def aws_metric_card(label: str, value: str, delta: str = None, icon: str = "📊"):
        """Create pastel blue styled metric card with icon"""
        delta_html = f'<div style="color: #4caf50; margin-top: 0.5rem;">{delta}</div>' if delta else ''
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #F5FAFF 100%); 
                    padding: 1.5rem; border-radius: 12px; 
                    border: 2px solid #B3E5FC; box-shadow: 0 2px 8px rgba(179, 229, 252, 0.2);">
            <div style="color: #1a1a1a; font-weight: 600; font-size: 14px; margin-bottom: 0.5rem;">
                {icon} {label}
            </div>
            <div style="color: #1a1a1a; font-weight: 700; font-size: 32px;">
                {value}
            </div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
