import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tqdm import tqdm
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveJsonSplitter
from src.llm_model.gemini_model import embedding_model
from src.config import VECTORDB_DIR
from src.utils import get_driver



class DataLoader:
    
    def __init__(self):

        self.embeddings = embedding_model()
        self.driver = get_driver()
        self.vector_db = Chroma(persist_directory=VECTORDB_DIR,embedding_function=self.embeddings)

        self.cypher_query = """
        MATCH (p) -[:HAS_INSTANCE]->(w)-[:HAS_DETAIL]->(d)-[:HAS_CONCEPT]->(c)
        WHERE p.name in ['Acne','AIDS','Acute myocardial infarction','Anxiety algorithm', 'Chronic Cystitis', 'Acute Kidney Injury','BMI','Blood Pressure','Cardiac Failure','Down Syndrome','HIV','Lung Cancer','Peanut Allergy','Sickle-cell anaemia','Wheezing']
        RETURN 
        p.name AS pname,
        properties(p) AS phenotype_props,
        properties(w) AS website_props,
        properties(d) AS detail_props,
        properties(c) AS concept_props
        """

    def extract_data(self,tx):
        return tx.run(self.cypher_query).data()

    def get_records(self):
        with self.driver.session() as session:
            print("Extracting Data")
            records = session.execute_read(self.extract_data)
            print("Data Extraction Completed")

            for record in records:
                record['pname'] = record['pname'].lower()
                record['website_props']['name'] = record['website_props']['name'].lower()

        return records

    def data_chuncking(self,records):
        document = []

        for json_data in records :
            pname = json_data["pname"]
            website = json_data["website_props"]["name"]
            splitter = RecursiveJsonSplitter(min_chunk_size=1000, max_chunk_size=1000)
            chunk = splitter.split_text(json_data, convert_lists=True)
            
            for _, text in enumerate(chunk):
                document.append(Document(page_content=str(text), 
                metadata={"phenotype_name": pname, "website_name" : website }))
        print("Chunking Completed")
        return document
    

    def get_vector_db(self):
        return self.vector_db

if __name__ == "__main__":

    dataloader = DataLoader()
    records = dataloader.get_records()
    document = dataloader.data_chuncking(records)
    vector_db = dataloader.get_vector_db()

    # Process documents in batches
    BATCH_SIZE = 500
    for i in tqdm(range(0, len(document), BATCH_SIZE), desc="Embedding Batches"):
        batch = document[i:i + BATCH_SIZE]  # Get batch slice
        vector_db.add_documents(batch)


