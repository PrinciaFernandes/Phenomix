from langchain_neo4j import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from src.utils import get_graph
from models.llm_model.gemini_model import chat_model
from models.prompts.Prompts import cypher_prompt,query_generation_template
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

Cypher_template = query_generation_template()

Cypher_query = PromptTemplate(
    template= Cypher_template,
    input_variables=["question"]
)

def get_cypher(query):
    response = llm.invoke(Cypher_query.invoke({"question":query}))
    return response.content