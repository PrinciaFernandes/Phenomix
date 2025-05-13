from langchain_neo4j import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from src.utils import get_graph
from models.llm_model.gemini_model import chat_model
from models.prompts.Prompts import cypher_prompt
# st.title("Phenomix Assistant")

llm = chat_model()
graph = get_graph()
 
Cypher_generation_template = cypher_prompt()

Cypher_generation_prompt = PromptTemplate(
    template= Cypher_generation_template,
    input_variables=["schema", "question"]
)

Cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph = graph,
    cypher_prompt= Cypher_generation_prompt,
    verbose = True,
    allow_dangerous_requests = True
)

def dynamic_search(query):
    result = Cypher_chain.invoke({"query" : query})
    return result

Cypher_template = """
You are a skilled Neo4j Cypher developer. Your task is to translate a natural language question about phenotypes into an accurate Cypher query. The data is organized in a graph database with interconnected nodes such as Phenotype, Website, Detail, and Concept. Use the schema provided to understand the relationships.

Instructions:
1. Parse the question and identify the target **phenotype** mentioned.
2. Locate the **Phenotype** node in the graph that matches the phenotype name.
3. From the **Phenotype**, traverse the following path:  
   Phenotype → Website → Detail → Concept  
   using the respective relationships.
4. At each node, identify and extract the relevant field(s) needed to answer the question.
5. Construct a Cypher query to fetch these fields. The query must cover all possible instances without any result limit.
6. The final output result should cyper query.

**Think carefully about which fields are required based on the question.**  
**Use WHERE clause filters for phenotype names or other constraints.**  
**RETURN only the fields that answer the question.**

---

Example 1:
Question: What is the PID of the phenotype 'Asthma'?  
Cypher Query:
MATCH (p:Phenotype)-[:HAS_INSTANCE]->(w:Website)-[:HAS_DETAIL]->(d:Detail)-[:HAS_CONCEPT]->(c:Concept)
WHERE p.name = 'Asthma'
RETURN w.PID AS PID

Example 2:
Question: Retrieve the Concept ID (CID) linked to phenotype 'Cancer'.
Cypher Query:
MATCH (p:Phenotype)-[:HAS_INSTANCE]->(w:Website)-[:HAS_DETAIL]->(d:Detail)-[:HAS_CONCEPT]->(c:Concept)
WHERE p.name = 'Cancer'
RETURN c.CID AS CID

User Question:{question}
"""

Cypher_query = PromptTemplate(
    template= Cypher_template,
    input_variables=["question"]
)

def get_cypher(query):
    response = llm.invoke(Cypher_query.invoke({"question":query}))
    return response.content