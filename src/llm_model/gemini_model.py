from src.utils import get_gemini_client
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
    

load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
client = get_gemini_client(api_key,base_url)

def get_json_response(prompt):
    response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
                {"role": "system", "content": 'You are a Helpful assistant.'},
                {"role": "user", "content": prompt}
            ],
            response_format={'type': 'json_object'}
        )
    return response.choices[0].message.content

def chat_model():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    return llm

def embedding_moedel():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)
    return embeddings

