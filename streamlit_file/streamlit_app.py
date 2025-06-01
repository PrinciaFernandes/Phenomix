import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

# Enhanced page configuration (rest remains the same)
st.set_page_config(
    page_title="PHENOTYPE EXPLORER",
    layout="wide",
    page_icon="🧬",
    initial_sidebar_state="expanded"
)

# Import the CSS function from style.py
from style import apply_custom_css

import time
from views.phenosearch import pheno_search
from views.graph import graph_view
from views.table import table_view
from views.dynamic import dynamic_search, get_cypher

# Apply the custom CSS
apply_custom_css()

# Enhanced sidebar with better styling
with st.sidebar:
    try:
        st.image(r'streamlit_file\assets\icon.png', use_container_width=True)
    except:
        st.markdown("🧬", unsafe_allow_html=True)  # Fallback icon with better styling
    st.markdown("</div>", unsafe_allow_html=True)

    page = st.radio(
        "🌌 Navigation",
        ["Phenomix Explorer", "Phenomix Assistant"],
        index=0,
        help="Choose your exploration mode for advanced phenotype analysis"
    )

if page == 'Phenomix Explorer':
    # Enhanced title with animation
    st.markdown("<h1 class='main-title'>PHENOTYPE EXPLORER</h1>", unsafe_allow_html=True)

    # Add a subtle divider
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Enhanced input with better UX
    st.markdown("<div style='margin: 1.5rem 0; font-size: 2rem; '>", unsafe_allow_html=True)
    phenotype_input = st.text_input(
        "ENTER PHENOTYPE:",
        placeholder="Search phenotypes (e.g., COPD, Asthma, Diabetes)...",
        help="Enter the name of the phenotype you want to analyze in detail"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Enhanced button layout with better spacing
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        button1 = st.button("📄 Document View", key="document_button", use_container_width=True)
    with col2:
        button2 = st.button("📊 Table View", key="table_button", use_container_width=True)
    with col3:
        button3 = st.button("🕸️ Graph View", key="graph_button", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Session state management (unchanged logic)
    if "document_clicked" not in st.session_state:
        st.session_state.document_clicked = False
    if "table_clicked" not in st.session_state:
        st.session_state.table_clicked = False
    if "graph_clicked" not in st.session_state:
        st.session_state.graph_clicked = False

    if button1:
        st.session_state.document_clicked = True
        st.session_state.table_clicked = False
        st.session_state.graph_clicked = False

    if button2:
        st.session_state.table_clicked = True
        st.session_state.document_clicked = False
        st.session_state.graph_clicked = False

    if button3:
        st.session_state.graph_clicked = True
        st.session_state.document_clicked = False
        st.session_state.table_clicked = False

    # Add loading animation and better error handling
    if st.session_state.document_clicked and phenotype_input:
        with st.spinner('🔍 Fetching document view...'):
            try:
                pheno_search(phenotype_input)
            except Exception as e:
                st.error(f"⚠️ Error loading document view: {e}")

    if st.session_state.table_clicked and phenotype_input:
        with st.spinner('📊 Generating table view...'):
            try:
                table_view(phenotype_input)
            except Exception as e:
                st.error(f"⚠️ Error generating table view: {e}")

    if st.session_state.graph_clicked and phenotype_input:
        with st.spinner('🕸️ Building graph visualization...'):
            try:
                graph_view(phenotype_input)
            except Exception as e:
                st.error(f"⚠️ Error building graph view: {e}")

elif page == 'Phenomix Assistant':
    # Enhanced assistant page
    st.markdown("<h1 class='assistant-title'> PHENOMIX ASSISTANT</h1>", unsafe_allow_html=True)
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

    # Enhanced example questions section
    st.markdown("""
    <div class='example-questions'>
        <h3>💡 Try Asking These:</h3>
        <div style='line-height: 1.7;'>
            <p><strong>1.</strong> What is the definition of 'COPD'?</p>
            <p><strong>2.</strong> Which websites mention 'Asthma'?</p>
            <p><strong>3.</strong> What phenotype has the ID 'CP000002'?</p>
            <p><strong>4.</strong> How many phenotypes are in the 'PHEKB' database?</p>
            <p><strong>5.</strong> Tell me about the data sources for 'Anxiety Disorder'.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Enhanced chat input
    query =st.chat_input("Ask me anything about phenotypes...")
    if query:
        with st.spinner('🧠 Processing...'):
            response = dynamic_search(query)
            cypher = get_cypher(query)
            st.session_state.chat_history.append((query, response, cypher))

    # Enhanced chat display
    if st.session_state.chat_history:
        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)
        for i, (user_input, result, query_cypher) in enumerate(st.session_state.chat_history):
            query_result = result['result']

            # User message
            with st.expander(f"👤 You asked:", expanded=True):
                st.markdown(f"**{user_input}**")

            # Assistant response
            with st.expander(f"🤖 Assistant replied:", expanded=True):
                st.markdown(query_result)

            # Cypher query (for developers)
            with st.expander(f"⚙️ Generated Cypher:", expanded=False):
                st.code(query_cypher, language='cypher')

            # Add separator between conversations
            if i < len(st.session_state.chat_history) - 1:
                st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

# Add enhanced footer for dark theme
if page == 'Phenomix Explorer':
    st.markdown("""
    <div class='footer-container'>
        <div class='footer-content'>
            <p>
                Exploring the Landscape of Phenotypes
            </p>
            <p class='crafted-with'>
                Crafted with <span class='heart'>❤️</span> for Discovery
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)