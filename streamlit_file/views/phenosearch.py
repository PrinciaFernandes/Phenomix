import streamlit as st
from src.utils import get_driver

driver = get_driver()

def get_websites(phenotype_name):
    with driver.session() as session:
        phenotype = f"(?i){phenotype_name}"
        result = session.run("""
            MATCH (p:Phenotype)-[:HAS_INSTANCE]->(w:Website)
            WHERE p.name =~ $name
            RETURN DISTINCT w.name AS website
        """, name=phenotype)
        websites = [record["website"] for record in result]
        return [""] + websites 


def get_pids(phenotype_name, website_name):
    with driver.session() as session:
        phenotype = f"(?i){phenotype_name}"
        result = session.run("""
            MATCH (p:Phenotype)-[:HAS_INSTANCE]->(w:Website {name: $website})
            MATCH (w)-[:HAS_DETAIL]->(d:Detail)
            WHERE p.name =~ $name
            RETURN DISTINCT d.PID AS pid, properties(d) AS detail_props
        """, name=phenotype, website=website_name)
        pid_list = [{"pid": record["pid"], "props": record["detail_props"]} for record in result]
        return [{"pid": "", "props": {}}] + pid_list 

def get_concepts_for_pid(pid):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Detail {PID: $pid})-[:HAS_CONCEPT]->(c:Concept)
            RETURN properties(c) AS concept_props
        """, pid=pid)
        return [record["concept_props"] for record in result]

def pheno_search(phenotype_input):
    websites = get_websites(phenotype_input)

    if len(websites) > 1:
        selected_website = st.selectbox("Select Website:", websites, key="search_website")
        
        if selected_website:
            pid_data = get_pids(phenotype_input, selected_website)
            pid_options = [item["pid"] for item in pid_data]

            if len(pid_options) > 1:
                selected_pid = st.selectbox("Select PID:", pid_options, key="search_pid")

                selected_detail = next((item["props"] for item in pid_data if item["pid"] == selected_pid), None)
                related_concepts = get_concepts_for_pid(selected_pid)

                if selected_website != "" and selected_pid != "":
                    # Detail section
                    st.subheader(f"📄 Detail for PID: {selected_pid}")
                    
                    # Create detail properties display
                    detail_text = "<br>".join([f"<b>{k}:</b> {v}" for k, v in selected_detail.items()])
                    
                    st.markdown(
                        f"""
                        <div class='detail-container'>
                            <b>Detail Properties:</b><br><br>
                            {detail_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Concepts section
                    st.subheader(f"🗃️ Concepts for PID: {selected_pid}")
                    
                    if related_concepts:
                        concept_html = ""
                        for i, concept in enumerate(related_concepts):
                            concept_html += f"<b>Concept {i+1}:</b><br>"
                            concept_html += "<br>".join([f"<b>{k}:</b> {v}" for k, v in concept.items()])
                            concept_html += "<br><hr style='margin: 10px 0;'>"
                        
                        st.markdown(
                            f"""
                            <div class='concept-container'>
                                {concept_html}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.info("⚠️ No related concepts found.")
    else:
        st.warning("⚠️ No websites found for this phenotype.")