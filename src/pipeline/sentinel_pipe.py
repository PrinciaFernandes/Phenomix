from src.utils import save_json,save_detail,save_concept
from src.config import RAW_DIR,SENTINEL_URL,SENTINEL_DIR

from src.scraping.sentinel_webscrapping import sentinel_scrapping
from src.processing.sentinel_concept_detail import get_detail, get_concept
from src.logger import get_logger
import json

logger = get_logger(__name__)

class SentinalPipeline:

    def __init__(self):
        self.detail = None
        self.concept = None

    def main(self):
        try:
            logger.info("SCRAPPING SENTINEL phenotypes...")
            base_url = SENTINEL_URL
            sentinel = sentinel_scrapping(base_url)
            logger.info("SCRAPPING SENTINEL done successfully")
            save_json(RAW_DIR,sentinel,'SENTINEL')
        except:    
            logger.exception("ERROR while scrapping SENTINEL phenotypes")


        try:
            logger.info("Creating SENTINEL detail file...")
            self.detail = get_detail(sentinel)
            logger.info("SENTINEL detail file Created Successfully...")
            save_detail(SENTINEL_DIR,self.detail,'SENTINEL')
        except:
           logger.exception("ERROR while creating SENTINEL detail file")            

        try:
            logger.info("Creating SENTINEL concept file...")
            self.concept = get_concept(sentinel,self.detail)
            logger.info("SENTINEL concept file Created Successfully...")
            save_concept(SENTINEL_DIR,self.concept,'SENTINEL')
        except:
            logger.exception("ERROR while creating SENTINEL concept file")

    
