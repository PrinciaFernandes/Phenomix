import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* Simple dark theme styling */
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        /* Main container styling */
        .main .block-container {
            padding: 2rem;
            max-width: 1200px;
            background-color: #2d2d2d;
            border-radius: 10px;
            margin: 1rem auto;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-1cypcdb {
            background-color: #262626 !important;
            border-right: 2px solid #2debfc;
        }
        
        /* Text color adjustments */
        .stMarkdown, .stText, p, span, div, label {
            color: #ffffff !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #404040;
            color: white;
            border: 2px solid #2debfc;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: #505050;
            border-color: #5afc03;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: #404040;
            color: white;
            border: 2px solid #2debfc;
        }
        
        /* Text input styling */
        .stTextInput > div > div > input {
            background-color: #404040;
            color: white;
            border: 2px solid #2debfc;
        }
        
        /* Chat input styling */
        .stChatInput > div > div > input {
            background-color: #404040;
            color: white;
            border: 2px solid #2debfc;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            background-color: #2d2d2d;
        }
        
        /* Code block styling */
        .stCodeBlock {
            background-color: #1a1a1a;
            border: 1px solid #5afc03;
            border-radius: 5px;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background-color: #5afc03;
            color: white;
        }
        
        .streamlit-expanderContent {
            background-color: #2d2d2d;
            border: 1px solid #404040;
        }
        
        /* Radio button styling */
        .stRadio > div {
            background-color: #404040;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
        
        /* Sidebar radio button text */
        .css-1d391kg .stRadio > div > label, 
        .css-1cypcdb .stRadio > div > label {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Container with border styling for details */
        .detail-container {
            background-color: #1a1a1a;
            border: 2px solid #5afc03;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            max-height: 200px;
            overflow-y: auto;
            color: #ffffff;
        }
        
        .concept-container {
            background-color: #1a1a1a;
            border: 2px solid #5afc03;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            max-height: 300px;
            overflow-y: auto;
            color: #ffffff;
        }
        
        /* Simple hover effects */
        .stButton > button:hover,
        .stSelectbox:hover,
        .stTextInput:hover {
            transform: translateY(-1px);
        }
    </style>
    """, unsafe_allow_html=True)