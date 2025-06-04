from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup
from datetime import datetime


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


def phekb_scrapping(base_url: str):
    print("Entered Scraping PHEKB")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(base_url)
    print(base_url)
    time.sleep(3)  
    all_links = []
    while True:
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody.p-datatable-tbody tr.ng-star-inserted")

        for row in rows:
            try:
                title_element = row.find_element(By.CSS_SELECTOR, "td.ng-star-inserted a")
                title = title_element.text.strip()
                url = title_element.get_attribute("href")
                all_links.append((title, url))
            except Exception as e:
                print("Error extracting data:", e)
        
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "button.p-paginator-next")
            if "p-disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(3)
        except Exception as e:
            print("Pagination finished or error:", e)
            break
    phekb = process_all_links(all_links,driver)
    driver.quit()
    return phekb

def extract_list(soup,selector):
    elements = soup.select(selector)
    return ', '.join([el.get_text(strip=True) for el in elements] if elements else ["NA"])

def process_all_links(all_links,driver):
    
    phenotypes_dictionary = []
    i = 0
    for title, url in all_links:  
        i +=1
        print(f"{i}:",title)
        driver.get(url)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        phenotype_id = soup.select_one("div.field-name-field-phenotype-id div.field-items").get_text(strip=True) if soup.select_one("div.field-name-field-phenotype-id div.field-items") else "NA"
        name = soup.select_one("h1.title").get_text(strip=True) if soup.select_one("h1.title") else "NA"
        description = soup.select_one("div.field-name-body div.field-items").get_text(strip=True) if soup.select_one("div.field-name-body div.field-items") else "NA"
        status = soup.select_one("div.field-name-field-p-status div.field-items").get_text(strip=True) if soup.select_one("div.field-name-field-p-status div.field-items") else "NA"
        authors = extract_list(soup,"div.field-name-field-author div.field-items div.field-item")
        phenotype_attributes = extract_list(soup,"div.field-name-field-class div.field-items div.field-item")
        institutions = extract_list(soup,"div.field-name-field-institution div.field-items div.field-item")
        networks = extract_list(soup,"div.field-name-field-network-associations div.field-items div.field-item")
        age = extract_list(soup,"div.field-name-field-ages div.field-items div.field-item")
        races = extract_list(soup,"div.field-name-field-race div.field-items div.field-item")
        gender = extract_list(soup,"div.field-name-field-gender div.field-items div.field-item")
        type_of_phenotype = extract_list(soup,"div.field-name-field-pgx-type div.field-items")

        date_created = soup.select_one("div.field-name-field-created-at .field-items").get_text(strip=True) if soup.select_one("div.field-name-field-created-at .field-items") else "NA"
        date_new = datetime.strptime(date_created,"%A, %B %d, %Y")
        formatted_date = date_new.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        
        files_section = soup.select_one("div.field-name-field-files div.field-items")
        files = {}
        if files_section:
            file_links = files_section.find_all("a")
            for file in file_links:
                files[file.get_text(strip=True)] = file.get("href", "NA")
        else:
            files = {"NA": "NA"}
        
        phenotype_data = {
            "Phenotype_id": int(phenotype_id),
            "Name": name,
            "Description": description,
            "Status": status,
            "Type_of_phenotype": type_of_phenotype ,
            "Phenotype_attributes": phenotype_attributes,
            "Authors": authors if authors != ["NA"] else ["NA"],
            "Files": files,
            "Institutions": institutions,
            "Ages": age ,
            "Races": races ,
            "Genders": gender ,
            "Networks": networks ,
            "Date_created": formatted_date
        }

        phenotypes_dictionary.append(phenotype_data)

    return phenotypes_dictionary
