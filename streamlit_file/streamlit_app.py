import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st

# Simple page configuration
st.set_page_config(
    page_title="PHENOTYPE EXPLORER",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the CSS function from style.py
from style import apply_custom_css
from views.phenosearch import pheno_search
from views.graph import graph_view
from views.table import table_view
from views.dynamic import dynamic_search, get_cypher
from views.chatbot import ChatBot

# Apply the custom CSS
apply_custom_css()

# Simple sidebar
with st.sidebar:
    try:
        st.image(r'streamlit_file\assets\icon.png', use_container_width=True)
    except:
        st.markdown("🧬")
    
    page = st.radio(
        "**NAVIGATION**",
        ["Phenomix Explorer", "Phenomix Assistant","Phenomix ChatBot"],
        index=0
    )

if page == 'Phenomix Explorer':
    # Simple title
    st.markdown("<h1 style='text-align: center;'>🔍 PHENOTYPE EXPLORER</h1>", unsafe_allow_html=True)
    st.divider()

    # Simple input
    phenotype_input = st.text_input(
        "**ENTER PHENOTYPE:**",
        placeholder="Search phenotypes (e.g., AIDS, Acne, HIV)...",
        help="Enter the name of the phenotype you want to analyze"
    )

    # Simple button layout
    col1, col2, col3 = st.columns(3)

    with col1:
        button1 = st.button("📄 Document View", key="document_button", use_container_width=True)
    with col2:
        button2 = st.button("📊 Table View", key="table_button", use_container_width=True)
    with col3:
        button3 = st.button("🕸️ Graph View", key="graph_button", use_container_width=True)

    # Session state management
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

    # Display views with simple loading
    if st.session_state.document_clicked and phenotype_input:
        with st.spinner('Loading document view...'):
            try:
                pheno_search(phenotype_input)
            except Exception as e:
                st.error(f"Error loading document view: {e}")

    if st.session_state.table_clicked and phenotype_input:
        with st.spinner('Loading table view...'):
            try:
                table_view(phenotype_input)
            except Exception as e:
                st.error(f"Error generating table view: {e}")

    if st.session_state.graph_clicked and phenotype_input:
        with st.spinner('Loading graph visualization...'):
            try:
                graph_view(phenotype_input)
            except Exception as e:
                st.error(f"Error building graph view: {e}")

elif page == 'Phenomix Assistant':
    # Simple assistant page
    st.markdown("<h1 style='text-align: center;'>👨‍💻 PHENOMIX ASSISTANT</h1>", unsafe_allow_html=True)
    st.divider()

    # Simple example questions
    with st.expander("💡 Example Questions", expanded=True):
        st.markdown("""
        **Try asking these questions:**
        1. What is the definition of 'COPD'?
        2. Which websites mention 'Asthma'?
        3. What phenotype has the detail PID 'CP000002'?
        4. How many phenotypes are in the 'PHEKB' database?
        5. Tell me about the data sources for 'Anxiety Disorder'.
        """)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Simple chat input
    query = st.chat_input("Ask me anything about phenotypes...")
    
    if query:
        with st.spinner('Processing your question...'):
            response = dynamic_search(query)
            cypher = get_cypher(query)
            st.session_state.chat_history.append((query, response, cypher))

    # Simple chat display
    if st.session_state.chat_history:
        st.subheader("Chat History")
        
        for i, (user_input, result, query_cypher) in enumerate(st.session_state.chat_history):
            query_result = result['result']

            # User message
            with st.container():
                st.markdown(f"**👤 You:** {user_input}")
                
                # Assistant response
                st.markdown(f"**🤖 Assistant:** {query_result}")
                
                # Cypher query (collapsible)
                with st.expander("View Generated Cypher Query"):
                    st.code(query_cypher, language='sql')
                
                st.divider()

elif page == 'Phenomix ChatBot':
    st.markdown("<h1 style='text-align: center;'> 🌐 PHENOMIX CHATBOT</h1>", unsafe_allow_html=True)
    st.divider()

    with st.expander("💡 Example Questions", expanded=True):
        st.markdown("""
        **Try asking these questions:**
        1. Give a brief on Peanut Allergy?
        2. What are PID of Acne?
        """)

   
    # Initialize chat history
    if "init" not in st.session_state:
        st.session_state.init = True
        st.session_state.chat_h = []
        st.session_state.dataset = []

    chatbot = ChatBot()
    # Simple chat input
    query = st.chat_input("Ask me anything about phenotypes...")
    
    

    if query:
        with st.container():
            if st.session_state.chat_h:
           
                for chat in st.session_state.chat_h:
                    with st.chat_message(chat["role"]):
                        st.markdown(chat["content"])

            st.chat_message("User").write(query)

            with st.spinner('Processing your question...'):
                query, response, retrieved_contexts,reference = chatbot.get_result(query)
            
            data = {
            "user_input":[query],
            "response":[response],
            "retrieved_contexts":[retrieved_contexts],
            "reference":[reference]
            }
            st.session_state.dataset.append(data)
            st.session_state.chat_h.append({"role":"User", "content":query})
            st.chat_message("Assistant").write(response)
            st.session_state.chat_h.append({"role":"Assistant", "content":response})




    

        