import json
import os
from openai import OpenAI
from pyconceptlibraryclient import Client
from neo4j import GraphDatabase
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

def save_json(dir,data,title):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(rf'{dir}\{title}_phenotypes.json','w') as file:
        json.dump(data,file,indent = 4)

def save_detail(dir,data,title):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(rf'{dir}\{title}_detail.json','w') as file:
        json.dump(data,file,indent=4)

def save_concept(dir,data,title):
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(rf'{dir}\{title}_concept.json','w') as file:
        json.dump(data,file,indent=4)

def get_gemini_client(api_key, base_url):
    GEMINI_CLIENT = OpenAI(
        api_key = api_key,
        base_url= base_url
    )
    return GEMINI_CLIENT

def get_hdruk_client():
    HDRUK_CLIENT = Client(public=True)
    return HDRUK_CLIENT

def get_driver():
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    return driver

def get_graph():
    graph = Neo4jGraph(neo4j_uri, neo4j_username, neo4j_password)
    return graph