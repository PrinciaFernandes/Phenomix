import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
from src.utils import get_driver

driver = get_driver()

def get_graph_data(tx,name):
    query = """
    MATCH (p:Phenotype{name:$name})-[:HAS_INSTANCE]->(w)-[:HAS_DETAIL]->(d)-[:HAS_CONCEPT]->(c)
    RETURN p, w, d, c
    """
    return list(tx.run(query, name=name))

def build_graph(records):
    G = nx.MultiDiGraph()
    for record in records:
        p = record["p"]
        w = record["w"]
        d = record["d"]
        c = record["c"]
 
        G.add_node(p.element_id, label=p["name"], group="Phenotype")
        G.add_node(w.element_id, label=w["name"], group="Website")
        G.add_node(d.element_id, label=d["PID"], group="Detail")
        G.add_node(c.element_id, label=c["CID"], group="Concept")

        G.add_edge(p.element_id, w.element_id, label="HAS_INSTANCE")
        G.add_edge(w.element_id, d.element_id, label="HAS_DETAIL")
        G.add_edge(d.element_id, c.element_id, label="HAS_CONCEPT")

    return G

def draw_pyvis_graph(G):
    net = Network(height="750px", width="100%", notebook=False)
    net.from_nx(G)
    net.repulsion(node_distance=120)    
    return net.generate_html()



def graph_view(phenotype_name):
    if phenotype_name:
        with driver.session() as session:   
            records = session.execute_read(get_graph_data, phenotype_name)

            if records:
                G = build_graph(records)
                html_content = draw_pyvis_graph(G)
                components.html(html_content, height=750)
            else:
                st.warning("No data found for this phenotype.")

