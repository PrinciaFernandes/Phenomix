import requests
from bs4 import BeautifulSoup


def hdruk_scrapping(base_url,client):
    hdruk = []

    for page in range(1,62):
        url = f"{base_url}{page}"
        response = requests.get(url)
        print("Page:",page)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all phenotype titles
            titles = soup.find_all("h3", class_="entity-card__title")

            for title in titles:
                phenotype_text = title.text.strip()
                phenotype_id = phenotype_text.split()[0] 
                # print(phenotype_id)
                phenotype_detail = client.phenotypes.get_detail(phenotype_id)
                try:
                    phenotype_concept = client.phenotypes.get_codelist(phenotype_id)
                except:
                    phenotype_concept = []

                phenotype_dictionary = {}
                phenotype_dictionary['phenotype_id']= phenotype_detail[0]['phenotype_id']
                phenotype_dictionary['version_id'] = phenotype_detail[0]['phenotype_version_id']
                phenotype_dictionary['details'] = phenotype_detail
                phenotype_dictionary['codelist'] = phenotype_concept
                
                hdruk.append(phenotype_dictionary)    
             
        else:
            return f"Failed to access page {page}"

    return hdruk  