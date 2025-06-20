import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import json
import pandas as pd
from src.llm_model.gemini_model import get_json_response
from src.prompts.Prompts import prompt_overview,prompt_description

TOKEN = []

def overview_extract(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        overview_page = ''

        for page in pdf.pages[:4]:
            text = page.extract_text()
            if 'Overview' in text:
                overview_page += text    
            if ' Request Send Date' in text and  'Glossary' not in text: 
                overview_page += text   

        response = get_json_response(prompt_overview(overview_page))
        overview = response.choices[0].message.content
        TOKEN.append(response.usage.to_dict())


    return overview

def description_extract(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        description_dict = []
        chunk_size = 5
        pages = len(pdf.pages)
        chunks = [range(i,i+chunk_size) if i + chunk_size <= pages else range(i,pages) for i in range(3,pages,chunk_size) ]
        for chunk in chunks:
            extracted = ''
            extracted_data = []
            for each_page in chunk:
                page = pdf.pages[each_page]
                text = page.extract_text()
                if not 'Glossary' in text and not 'Generic Name' in text and not 'Brand Name' in text:
                    if len((extracted + text).split()) < 5000:
                        extracted += text
                    else:
                        extracted_data.append(text)
            if extracted != '':
                extracted_data.insert(0,extracted)
            for text in extracted_data:
                response = get_json_response(prompt_description(text))
                description = response.choices[0].message.content
                TOKEN.append(response.usage.to_dict())

                description_new = json.loads(description.replace("\n",''))
                if len(description_new) > 1:
                    phenotype_description = []
                    codes = description_new
                    columns = codes[0].split("|")
                    for row in codes[1:]:
                        rows = row.split("|")
                        dictionary = {key:value for key,value in zip(columns,rows)}
                        phenotype_description.append(dictionary)
                    description_dict += phenotype_description
                else:
                    continue
    return description_dict

def extract_exceptionl(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:   
        extracted_text = ''
        for page in pdf.pages:
            text = page.extract_text()
            if 'Overview' in text:
                pass  
            if ' Request Send Date' in text and  'Glossary' not in text: 
                pass
            else:
                extracted_text += text
        overview = overview_extract(pdf_path)
        
        response = get_json_response(prompt_description(extracted_text))
        description = response.choices[0].message.content
        TOKEN.append(response.usage.to_dict())
        description_json = json.loads(description.replace("\n",''))
        if len(description_json) > 1:
            phenotype = []
            codes = description_json
            columns = codes[0].split("|")
            for row in codes[1:]:
                rows = row.split("|")
                code_dictionary ={key:value for key,value in zip(columns,rows)}
                phenotype.append(code_dictionary)
    phenotype_dict = json.loads(overview)
    phenotype_dict["Code_Description"] = phenotype
    return phenotype_dict

def phenotype(pdf_url):
    response = requests.get(pdf_url)
    pdf_content = response.content
    pdf_path = io.BytesIO(pdf_content)
    try:
        if not 'algorithm_Critical_COVID_updated.pdf' in pdf_path:
            overview = overview_extract(pdf_path)
            description = description_extract(pdf_path)
            phenotype_dict = json.loads(overview)
            phenotype_dict['Code_Description'] = description
        else:
            phenotype_dict = extract_exceptionl(pdf_path)
    except:
        return f"Error in Calling PDF Extraction function for {pdf_url}"
    return phenotype_dict


def sentinel_scrapping(base_url: str):
    sentinel  = []
    df = pd.DataFrame(columns = ['Pdf_num'])
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    page_links = []
    for link in soup.find_all('a', href=True):
        if 'health-outcomes-interest/' in link['href']: 
            full_link = requests.compat.urljoin(base_url, link['href'])
            response = requests.get(full_link)
            if response.status_code == 200:
                soup_page = BeautifulSoup(response.text, 'html.parser')
                
                if "Outcomes Assessed in Inferential Analyses" in soup_page.get_text():
                    page_links.append(full_link)
        else:
            continue
    i = 0              
    for link in page_links[:5]:
        global TOKEN
        TOKEN = []
        content = requests.get(link)
        if content.status_code == 200:  
            soup_page = BeautifulSoup(content.text,'html.parser')
        for link in soup_page.find_all('a', href=True):
            
            if ".pdf" in link['href']: 
                i += 1
                pdf_link = requests.compat.urljoin(base_url, link['href'])
                sentinel_dict = phenotype(pdf_link)
                sentinel.append(sentinel_dict)
                print(f"{i}: {pdf_link}")
                token = pd.DataFrame(TOKEN)
                token['Pdf_num'] = i 
                df = pd.concat([df, token], ignore_index=True)
    df.to_excel(r'data/sentinel_token.xlsx', index=False)
    return sentinel


if __name__ == "__main__":
    base_url = "https://www.sentinelinitiative.org/methods-data-tools/health-outcomes-interest?1=Outcomes+Assessed+in+Inferential+Analyses"
    sentinel_scrapping(base_url)
    print("Sentinel Scrapping Completed")   