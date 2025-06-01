
import streamlit as st
import pandas as pd
from src.utils import get_driver

driver = get_driver()

# Get websites for a given phenotype
def get_websites(phenotype_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Phenotype {name: $name})-[:HAS_INSTANCE]->(w:Website)
            RETURN DISTINCT w.name AS website
        """, name=phenotype_name)
        websites = [record["website"] for record in result]
        return [""] + websites 

# Get all PID nodes (Details) for a website
def get_pids(phenotype_name, website_name):
    with driver.session() as session:
        result = session.run("""
            MATCH (p:Phenotype {name: $name})-[:HAS_INSTANCE]->(w:Website {name: $website})
            MATCH (w)-[:HAS_DETAIL]->(d:Detail)
            RETURN DISTINCT d.PID AS pid, properties(d) AS detail_props
        """, name=phenotype_name, website=website_name)
        pid_list =  [{"pid": record["pid"], "props": record["detail_props"]} for record in result]
        return [{"pid": "", "props": {}}] + pid_list 
    
def get_concepts_for_pid(pid):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Detail {PID: $pid})-[:HAS_CONCEPT]->(c:Concept)
            RETURN properties(c) AS concept_props
        """, pid=pid)
        concept_data = [record["concept_props"] for record in result]
        return pd.DataFrame(concept_data)

def table_view(phenotype_input):
    websites = get_websites(phenotype_input)

    if len(websites)>1:
        selected_website = st.selectbox("Select Website :", websites,key="table_website")

        if selected_website:
            pid_data = get_pids(phenotype_input, selected_website)
            pid_options = [item["pid"] for item in pid_data]

            if len(pid_options)>1:
                selected_pid = st.selectbox("Select PID", pid_options,key = 'table_pids')

                selected_detail = next((item["props"] for item in pid_data if item["pid"] == selected_pid), None)

                if selected_website != "" and selected_pid != "" :
                    # Detail Container
                    st.markdown(f"### 📄 Detail for PID: {selected_pid}")
                    st.markdown(
                        f"""
                        <div style='color: #ffffff; border: 2px solid #4CAF50; padding: 15px; height: 200px; overflow-y: auto;
                                    background-color:#000000 ; border-radius: 10px; margin-bottom: 20px;'>
                            <b>Detail Properties:</b><br>
                            {"<br>".join([f"{k}: {v}" for k, v in selected_detail.items()])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

<<<<<<< HEAD:streamlit/views/table.py
                # Detail Container
                st.markdown(f"### 📄 Detail for PID: {selected_pid}")
                st.markdown(
                    f"""
                    <div style='color: #000080; border: 2px solid #4CAF50; padding: 15px; height: 200px; overflow-y: auto;
                                background-color:#f4eeff ; border-radius: 10px; margin-bottom: 20px;'>
                        <b>Detail Properties:</b><br>
                        {"<br>".join([f"{key}: {value}" for key, value in selected_detail.items()])}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if selected_pid:
                # Concepts Container
                    st.markdown(f"### 🗃️ Concept table for PID: {selected_pid}")
                    related_concepts = get_concepts_for_pid(selected_pid)
                    st.dataframe(related_concepts,use_container_width=True,height=500)  
                    
=======
                    if selected_pid:
                    # Concepts Container
                        st.markdown(f"### 🗃️ Concept table for PID: {selected_pid}")
                        related_concepts = get_concepts_for_pid(selected_pid)
                        st.dataframe(related_concepts,use_container_width=True,height=500)  
                        
>>>>>>> 45543f2c4b357c8bc8cc729a21bca931af7b283d:streamlit_file/views/table.py
    else:
        st.warning("⚠️ No websites found for this phenotype.")