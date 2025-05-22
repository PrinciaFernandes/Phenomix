def prompt_overview(overview_page):
   return f'''
    Your task is to return a dictionary of the text {overview_page}
    The input content contains extracted text from a page of a PDF file:  
    - **Page 1:** Overview   
    Your task is to create a dictionary with the following structure:  
    First key is `phenotype`: The outcome of the phenotype( that is, value of the key `Outcome`).  
    Second key is `Overview`: A dictionary containing specific information extracted from the first page.  

    Extract text from the word **'Overview'** up to the words **'List of international diseases'**.  
    The `Overview` key should contain a dictionary with the following keys and their corresponding values:  
    - `Title`  
    - `Request IDs`  
    - `Description`  
    - `Outcome`  
    - `Algorithm to define outcome`  
    - `Query period`  
    - `Request to send dates`  

    *While extracting values for `Query period` and `Request to send dates`, do not include anything other than dates.Date format for these two vales will be like 'July 7, 2015'*
    Each value should be extracted as the text following the respective key (excluding escape characters like `\\n`).  
    Ensure the response does **not** contain escaped quotes (`\"`). 
    Provide the response without escape characters(no backslashes before quotes and after quotes).
    **Incase there is any sentence that contains `additional information`, exclude that sentence. **
    **Note:** Exclude any backslashes (`\\`) and newline characters (`\\n`) in the final response and replace those with single whitespace.
'''

def prompt_description(description_page):
    return f'''
    Your task is to return only a list from the text {description_page}.

    Input Details:
    The input consists of rows containing different diseases extracted from a PDF file. Your task is to create a list of multiple strings following the given structure:

    1. Extract text from "code description" or "codes description" up to the end of the page.
    2. Use the text before a newline (`\\n`) as the first row and the text after it as the following rows.
    3. The elements of the list should be multiple strings.

    Output Structure:
    Each string in the list should follow this format:
    "Code|Description|Code_Type|Code_Category"
    These four columns are mandatory in each row.

    - Code (Example: "K57.20" or "18.79", it can be either fully numeric or alphanumeric, but not fully alphabets like 'bleeding')
    - Description (Example: "Occlusion and stenosis of basilar artery with cerebral infarction")
    - Code_Type (Example: "ICD-9-CM")
    - Code_Category ( "Diagnosis" or "Procedure")

    Handling Multiline Descriptions:
    If a description spans multiple lines, do not split it into a new row, consider it as a single row.
    Example:
    "433.31 Occlusion and stenosis of multiple and bilateral precerebral arteries with cerebral ICD-9-CM Diagnosis infarction"
    The word "infarction" should remain in the same string as the code "433.31" and not move to the next row.

    Handling Missing Columns:
    If any of the four mandatory columns (Code, Description, Code_Type, Code_Category) is missing in a row, replace it with "None".
    Example: If Code_Category is missing:
    "433.01|Occlusion and stenosis of basilar artery with cerebral infarction|ICD-9-CM|None"
    If Code_Category column is missing in a row then, identify the code category from text before the words "code description" or "codes description" .
    If this is a text "International Classification of Diseases, Ninth Edition, Clinical Modification (ICD-9-CM) Diagnosis Codes, Generic Names, 
    and Healthcare Common Procedure Coding System (HCPCS) Codes Used to Define Clostridium Difficile in this Request", then Code_Category will be 'Diagnosis'.
    Thus find the code_category in the texts before the words "code description" or "codes description".

    Handling Extra Columns:
    If additional columns are present, include them.
    The minimum number of columns must always be four, but there could be five or more if extra columns exist.

    Special Cases:
    If Principal_Diagnosis and Care_Setting are present as column headers, include them in the output.
    If a row does not start with a code (e.g., "433.01"), assume None for the Code.
    Example:
    "None|NITAZOXANIDE|National Drug Code|ANY"

    Exclusions:
    Ignore disease explanations or general descriptions, such as:
    - "Intentional self-harm"
    - "Non-Cardiac Malformations"
    - "Clostridium difficile treatment dispensing within 7 days of encounter"
    Exclude the records under the column "Generic Name".
    DO NOT consider any texts or rows under the column name *'Generic Name'* and *'Brand Name'*.
    If the text has "Generic Name" or "Brand Name" exclude the records after it.

    Exclude any text enclosed in Italian formatting.
    Remove all backslashes (`\\`) and newline characters (`\\n`), replacing them with a single space.

    Final Output:
    A list of strings, where:
    - The first string is the column headers:
    "Code|Description|Code_Type|Code_Category"
    - Each subsequent string represents a disease record.

'''

def cypher_prompt():
    return """
You are a skilled Neo4j Cypher developer. Your task is to translate a natural language question about phenotypes into an accurate Cypher query. The data is organized in a graph database with interconnected nodes such as Phenotype, Website, Detail, and Concept. Use the schema provided to understand the relationships.

Instructions:
1. Parse the question and identify the target **phenotype** mentioned.
2. Locate the **Phenotype** node in the graph that matches the phenotype name.
3. From the **Phenotype**, traverse the following path:  
   Phenotype → Website → Detail → Concept  
   using the respective relationships.
4. At each node, identify and extract the relevant field(s) needed to answer the question.
5. Construct a Cypher query to fetch these fields. The query must cover all possible instances without any result limit.
6. The final output result should be neat manner if answer is in list or dictinary or in any other date format give it in simple human readable text format. 

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

Schema:{schema}
User Question:{question}
""" 
def query_generation_template():
    return"""
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