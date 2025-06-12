from langchain_core.output_parsers import JsonOutputParser
from langchain_chroma import Chroma
from src.prompts.Prompts import Filter_template ,Generator_template
from dotenv import load_dotenv
from src.llm_model.gemini_model import embedding_model,chat_model
from src.config import VECTORDB_DIR
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness,LLMContextRecall,LLMContextPrecisionWithReference,NoiseSensitivity
from ragas.llms import LangchainLLMWrapper
from src.logger import get_logger
import uuid


class ChatBot:
    def __init__(self):

        self.embeddings = embedding_model()
        self.vector_db = Chroma(embedding_function=self.embeddings, persist_directory=VECTORDB_DIR)
        self.llm = chat_model()
        self.parser = JsonOutputParser()
        self.filtering_chain = Filter_template | self.llm | self.parser
        self.generator_chain = Generator_template | self.llm
        self.evaluator_llm = LangchainLLMWrapper(self.llm)
        self.session_id = str(uuid.uuid4().hex)

    def get_result(self, query):
        logger = get_logger("ChatBot",self.session_id)
        self.query = query
        lower_query = query.lower()
        filtering_result = self.filtering_chain.invoke({"query" : lower_query})
        
        if filtering_result:
            metadata_filter = filtering_result
        else:
            metadata_filter = None
        retriever = self.vector_db.as_retriever(search_type="mmr", search_kwargs = {"k": 4, "filter":metadata_filter, 'fetch_k':1000})
        response = retriever.invoke(query)
        logger.info("RAG result retrieved successfully")
        retrieved_contexts = [f"content:{doc.page_content}, metadata: {doc.metadata} " for doc in response]
        
        reference = ', '.join([doc.page_content for doc in response])

        tupled_doc = [(doc.metadata,doc.page_content) for doc in response]

        result = self.generator_chain.invoke({"query": query, "content" : tupled_doc})

        self.ragas(query, result.content, retrieved_contexts,reference)
        return result.content
    

    def ragas(self,query,generated_response,retrieved_documents,reference):

        self.data = {
            "user_input":[query],
            "response":[generated_response],
            "retrieved_contexts":[retrieved_documents],
            "reference":[reference]
        }

        self.dataset = Dataset.from_dict(self.data)

        self.metrics = [
            Faithfulness(),
            LLMContextRecall(),
            LLMContextPrecisionWithReference(),
            NoiseSensitivity()
        ]

        result = evaluate(dataset=self.dataset,metrics=self.metrics,llm=self.evaluator_llm)
        
        print(result)
    

