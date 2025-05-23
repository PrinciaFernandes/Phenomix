
import streamlit as st
from src.utils import get_driver

driver = get_driver()

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

# Get concepts related to a given PID
def get_concepts_for_pid(pid):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Detail {PID: $pid})-[:HAS_CONCEPT]->(c:Concept)
            RETURN properties(c) AS concept_props
        """, pid=pid)
        return [record["concept_props"] for record in result]

def pheno_search(phenotype_input):
    websites = get_websites(phenotype_input)

    if len(websites)>1:
        selected_website = st.selectbox("Select Website :", websites,key="search_website")
        if selected_website:
            pid_data = get_pids(phenotype_input, selected_website)
            pid_options = [item["pid"] for item in pid_data]

            if len(pid_options)>1:
                selected_pid = st.selectbox("Select PID", pid_options,key = "Seacrh_pid")

                selected_detail = next((item["props"] for item in pid_data if item["pid"] == selected_pid), None)
                related_concepts = get_concepts_for_pid(selected_pid)

                if selected_website != "" and selected_pid != "" :
                    # Detail Container
                    st.markdown(f"### 📄 Detail for PID: {selected_pid}")
                    st.markdown(
                        f"""
                        <div style='color: #000080; border: 2px solid #4CAF50; padding: 15px; height: 200px; overflow-y: auto;
                                    background-color:#f4eeff ; border-radius: 10px; margin-bottom: 20px;'>
                            <b>Detail Properties:</b><br>
                            {"<br>".join([f"{k}: {v}" for k, v in selected_detail.items()])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Concepts Container
                    st.markdown(f"### 🗃️ Concepts for PID: {selected_pid}")
                    if related_concepts:
                        concept_html = "<br>".join([
                            f"<b>Concept {i+1}</b><br>" + "<br>".join([f"{k}: {v}" for k, v in c.items()]) + "<br><hr>"
                            for i, c in enumerate(related_concepts)
                        ])
                        st.markdown(
                            f"""
                            <div style='color: #000080; border: 2px solid #2196F3; padding: 15px; height: 300px; overflow-y: auto;
                                        background-color: #d9f2ff; border-radius: 10px;'>
                                {concept_html}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("⚠️ No related concepts found.")
    else:
        st.warning("⚠️ No websites found for this phenotype.")
