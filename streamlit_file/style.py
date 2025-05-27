import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

        /* Global styling with animated dark gradient background */
        .stApp {
            background: linear-gradient(315deg, #0b014f 0%, #1c013a 25%, #350353 50%, #52055b 75%, #76075e 100%);
            background-size: 400% 400%;
            animation: darkGradient 15s ease infinite;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            color: #f8f9fa;
        }

        @keyframes darkGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Main container with hover effect */
        .main .block-container {
            padding: 2.5rem 3.5rem;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(30px);
            border-radius: 25px;
            box-shadow:
                0 20px 40px rgba(0, 0, 0, 0.3),
                0 10px 20px rgba(0, 0, 0, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.1),
                inset 0 -1px 0 rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin: 2rem auto;
            max-width: 1200px;
            transform: perspective(800px) rotateX(5deg);
            transition: all 0.4s ease-in-out;
        }

        .main .block-container:hover {
            transform: perspective(800px) rotateX(0deg) translateY(-5px);
            box-shadow:
                0 25px 50px rgba(0, 0, 0, 0.35),
                0 12px 25px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        /* Enhanced Sidebar styling */
        .css-1d391kg, .css-1cypcdb {
            background: linear-gradient(180deg,
                rgba(11, 1, 79, 0.9) 0%,
                rgba(28, 1, 58, 0.9) 25%,
                rgba(53, 3, 83, 0.9) 50%,
                rgba(82, 5, 91, 0.9) 75%,
                rgba(118, 7, 94, 0.9) 100%) !important;
            backdrop-filter: blur(25px);
            border-right: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow:
                2px 0 15px rgba(0, 0, 0, 0.2),
                inset -1px 0 0 rgba(255, 255, 255, 0.05);
            position: relative;
            overflow: hidden;
        }

        /* Animated radial gradient overlay for sidebar */
        .css-1d391kg::before, .css-1cypcdb::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 60%),
                radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.03) 0%, transparent 60%);
            animation: sidebarRadial 12s linear infinite;
            pointer-events: none;
        }

        @keyframes sidebarRadial {
            0% { transform: rotate(0deg); opacity: 1; }
            100% { transform: rotate(360deg); opacity: 0.8; }
        }

        /* Sidebar content styling (radio buttons) with glassmorphism */
        .css-1d391kg .stRadio > div, .css-1cypcdb .stRadio > div {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(20px);
            border-radius: 15px;
            padding: 1rem 1.2rem !important;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin: 0.8rem 0 !important;
            box-shadow:
                0 8px 16px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
        }

        .css-1d391kg .stRadio > div:hover, .css-1cypcdb .stRadio > div:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            transform: translateY(-2px);
            box-shadow:
                0 10px 20px rgba(0, 0, 0, 0.15);
        }

        /* Sidebar title styling */
        .css-1d391kg .stRadio > label, .css-1cypcdb .stRadio > label {
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.3rem !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
            font-family: 'Poppins', sans-serif !important;
            margin-bottom: 1rem !important;
            text-align: center !important;
            display: block !important;
        }

        /* Sidebar radio button options text */
        .css-1d391kg .stRadio > div > label, .css-1cypcdb .stRadio > div > label {
            color: #e0f2f7 !important;
            font-weight: 500 !important;
            font-size: 1.05rem !important;
            text-shadow: 0.5px 0.5px 1px rgba(0,0,0,0.3) !important;
            margin: 0.4rem 0 !important;
            padding: 0.7rem 1rem !important;
            border-radius: 10px !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
            display: block !important;
        }

        .css-1d391kg .stRadio > div > label:hover, .css-1cypcdb .stRadio > div > label:hover {
            background: rgba(255, 255, 255, 0.05) !important;
            transform: translateX(3px) !important;
            text-shadow: 0.5px 0.5px 1.5px rgba(0,0,0,0.4) !important;
        }

        /* Enhanced title styling with gradient and subtle animation */
        .main-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: #ffffff; /* Set the main color to white */
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #4a148c, #7b1fa2, #9c27b0);
            -webkit-background-clip: text;
            /* -webkit-text-fill-color: transparent; */ /* Remove this line */
            background-size: 200% 200%;
            animation: gradientShift 5s ease infinite, titleFloat 5s ease-in-out infinite;
            transform: perspective(500px) rotateX(3deg);
            letter-spacing: -1px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
        }

        .main-title::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 150px;
            height: 3px;
            background: linear-gradient(90deg, transparent, #9c27b0, transparent);
            border-radius: 1.5px;
            animation: underlineGlow 3s ease infinite;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes titleFloat {
            0%, 100% { transform: perspective(500px) rotateX(3deg) translateY(0px); }
            50% { transform: perspective(500px) rotateX(3deg) translateY(-5px); }
        }

        @keyframes underlineGlow {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; box-shadow: 0 0 15px rgba(156, 39, 176, 0.7); }
        }

        /* Enhanced assistant title for dark theme */
        .assistant-title {
            font-size: 3.2rem;
            font-weight: 800;
            color: #ffffff; /* Set the main color to white */
            text-align: center;
            margin-bottom: 1.8rem;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #9c27b0, #7b1fa2, #4a148c);
            -webkit-background-clip: text;
            /* -webkit-text-fill-color: transparent; */ /* Remove this line */
            background-size: 200% 200%;
            animation: gradientShift 5s ease infinite;
            transform: perspective(500px) rotateX(3deg);
            letter-spacing: -1px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* Container animations */
        .element-container {
            animation: fadeIn 0.5s ease-out;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        /* Custom section dividers for dark theme */
        .section-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, #9c27b0, #7b1fa2, transparent);
            margin: 2.5rem 0;
            border-radius: 1px;
            box-shadow: 0 1px 4px rgba(156, 39, 176, 0.4);
        }

        /* Enhanced button container */
        .button-container {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin: 2rem 0;
        }

        /* Code block styling for dark theme */
        .stCodeBlock {
            background: rgba(30, 30, 30, 0.9);
            border-radius: 12px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            color: #f0f8ff !important; /* Light color for code text */
            padding: 1rem;
            overflow-x: auto;
        }

        /* Enhanced content text colors (overriding Streamlit defaults) */
        .stMarkdown, .stText, p, span, div, label {
            color: #f8f9fa !important;
        }

        /* Sidebar icon container styling for dark theme */
        .sidebar-icon-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.5rem;
            margin: 0.8rem 0 1.5rem 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow:
                0 8px 16px rgba(0, 0, 0, 0.1);
            font-size: 2.5rem;
            transition: all 0.3s ease-in-out;
        }

        .sidebar-icon-container:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow:
                0 10px 20px rgba(0, 0, 0, 0.15);
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Smooth transitions for all interactive elements */
        * {
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Enhanced example questions section */
        .example-questions {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }

        .example-questions h3 {
            color: #ffffff;
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }

        .example-questions p {
            color: #e0f2f7;
            margin-bottom: 0.5rem;
        }

        /* Enhanced footer for dark theme */
        .footer-container {
            text-align: center;
            padding: 2.5rem 0;
            margin-top: 3rem;
        }

        .footer-content {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            color: #e0f2f7;
            font-weight: 400;
            transform: perspective(500px) rotateX(2deg);
            transition: all 0.3s ease-in-out;
            margin: 0 auto;
            max-width: 600px;
        }

        .footer-content p {
            margin: 0;
            font-size: 1.3rem;
        }

        .footer-content .heart {
            color:#e91e63;
        }

        .footer-content .crafted-with {
            margin-top: 0.3rem;
            font-size: 1rem;
            color: #ccc;
            font-style: italic;
        }
    </style>
    """, unsafe_allow_html=True)