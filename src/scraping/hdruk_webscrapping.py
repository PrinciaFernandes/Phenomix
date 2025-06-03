import requests
from bs4 import BeautifulSoup


def hdruk_scrapping(base_url,client):
    hdruk = []
    response = requests.get(base_url)
    if response.status_code == 200: 
        soup = BeautifulSoup(response.content, 'html.parser')
        page_items = soup.select("ul.pagination-container__pages li")


        page_numbers = []
        for item in page_items:
            if "divider" in item.get("class", []):
                continue
            text = item.get_text(strip=True)
            if text.isdigit():
                page_numbers.append(int(text))

        page_number = min(page_numbers)

        for page in range(1, page_number + 1):
            all_titles = []
            res = requests.get(f"{base_url}?page={page}")
            soup = BeautifulSoup(res.content, "html.parser")
            
            links = soup.find_all('a', class_="entity-card__click",href = True)
            all_titles = [link.find('h3',class_ = "entity-card__title").string for link in links]

            for title in all_titles:
                phenotype_text = title.text.strip()
                phenotype_id = phenotype_text.split()[0] 
                phenotype_detail = client.phenotypes.get_detail(phenotype_id)
                print(phenotype_id)

                try:
                    phenotype_concept = client.phenotypes.get_codelist(phenotype_id)
                except:
                    phenotype_concept = []

                hdruk_dictionary = {}
                hdruk_dictionary['phenotype_id']= phenotype_detail[0]['phenotype_id']
                hdruk_dictionary['version_id'] = phenotype_detail[0]['phenotype_version_id']
                hdruk_dictionary['details'] = phenotype_detail
                hdruk_dictionary['codelist'] = phenotype_concept
                    
                hdruk.append(hdruk_dictionary)

        return hdruk
    else:
        return f"Failed to access HDRUK page"