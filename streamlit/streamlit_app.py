import streamlit as st
import time
from views.phenosearch import pheno_search
from views.graph import graph_view
from views.table import table_view
from views.dynamic import dynamic_search,get_cypher


st.set_page_config(page_title="Phenotype Explorer",layout="centered",page_icon=r"streamlit\assets\pheno_image.png")

st.sidebar.image(r'streamlit\assets\icon.png', use_container_width=True)
page = st.sidebar.radio("Pages",["Phenomix Explorer","Phenomix Assistant"],index = 0)

if page =='Phenomix Explorer':
    st.title("🔍︎ Phenotype Explorer")
    phenotype_input = st.text_input("Enter Phenotype Name :",None)

    col1,col2,col3=st.columns(3)
    with col1:
        button1 = st.button("Document view", key="document_button",use_container_width=True)
    with col2:
        button2 = st.button("Table view", key="table_button",use_container_width=True)
    with col3:    
        button3 = st.button("Graph view", key="graph_button",use_container_width=True)

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


    if st.session_state.document_clicked and phenotype_input:
        try:
            pheno_search(phenotype_input)
        except:
            st.warning("⚠️ Unable to load this phenotype")

    if st.session_state.table_clicked and phenotype_input:
        try:
            table_view(phenotype_input)
        except:
            st.warning("⚠️ Unable to load this phenotype")

    if st.session_state.graph_clicked and phenotype_input:
        try:
            graph_view(phenotype_input)
        except:
            st.warning("⚠️ Unable to load this phenotype")

elif page == 'Phenomix Assistant':
    st.title("👩🏻‍💻 Phenomix Assistant")
    st.write("Example Questions :  \n"
    "1.Give defination for the phenotype 'COPD'?  \n"
    "2.Give all website in which phenotype 'Asthma' is present?  \n"
    "3.What is the phenotype name of this PID='CP000002'?  \n"
    "4.How many phenotypes are there in 'PHEKB' website?  \n"
    "5.Give the data source and publications of phenotype 'Anxiety Disorder'?")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    query = st.chat_input("Your query")

    if query:
        response = dynamic_search(query)
        col1, col2 = st.columns(2)
        
        cypher = get_cypher(query)

        st.session_state.chat_history.append((query,response,cypher))
        container = st.container()
        
        for user_input, result, query in st.session_state.chat_history:
            query_result = result['result']

            with container.expander(f"You", expanded = True):
                st.markdown(user_input)

            with container.expander(f"Assistant", expanded = True):
                st.markdown(query_result)

            with container.expander(f"Cypher Query", expanded = True):
                st.markdown(query)
            