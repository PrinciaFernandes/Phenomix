
from src.config import RAW_DIR,HDRUK_URL,HDRUK_DIR
from src.utils import save_json,save_detail,save_concept,get_hdruk_client

from src.scraping.hdruk_webscrapping import hdruk_scrapping
from src.processing.hdruk_concept_detail import get_detail,get_concept
from src.logger import get_logger

logger = get_logger(__name__)

class HDRUKPipeline:

    def __init__(self):
        self.detail = None
        self.concept = None

    def main(self):
        try:
            logger.info("SCRAPPING HDRUK phenotypes...")
            base_url = HDRUK_URL
            client = get_hdruk_client()
            hdruk = hdruk_scrapping(base_url,client)
            logger.info("SCRAPPING HDRUK done successfully")
            save_json(RAW_DIR,hdruk,'HDRUK')
        except:
            logger.exception("ERROR while scrapping HDRUK phenotypes")

        try:
            logger.info("Creating HDRUK detail file...")
            self.detail = get_detail(hdruk)
            logger.info("HDRUK detail file Created Successfully...")
            save_detail(HDRUK_DIR,self.detail,'HDRUK')
        except:
           logger.exception("ERROR while creating HDRUK detail file")

        try: 
            logger.info("Creating HDRUK concept file...")
            self.concept = get_concept(hdruk,self.detail)
            logger.info("HDRUK concept file Created Successfully...")
            save_concept(HDRUK_DIR,self.concept,'HDRUK')        
        except:
            logger.exception("ERROR while creating HDRUK concept file")
