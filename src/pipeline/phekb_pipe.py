from src.utils import save_json,save_detail,save_concept
from src.config import RAW_DIR,PHEKB_URL,PHEKB_DIR

from src.scraping.phekb_webscrapping import phekb_scrapping
from src.processing.phekb_concept_detail import get_concept,get_detail
from src.logger import get_logger

logger = get_logger(__name__)

class PHEKBPipeline:

    def __init__(self):
        self.detail = None
        self.concept = None

    def main(self):
        try:
            logger.info("SCRAPPING PHEKB phenotypes...")
            base_url = PHEKB_URL
            phekb = phekb_scrapping(base_url)
            logger.info("SCRAPPING PHEKB done successfully")
            save_json(RAW_DIR,phekb,'PHEKB')
        except:
            logger.exception("ERROR while scrapping PHEKB phenotypes")
        
        try:
            logger.info("Creating PHEKB detail file...")
            self.detail = get_detail(phekb)
            logger.info("PHEKB detail file Created Successfully...")
            save_detail(PHEKB_DIR,self.detail,'PHEKB')
        except:
            logger.exception("ERROR while creating PHEKB detail file")

        try:
            logger.info("Creating PHEKB concept file...")
            self.concept = get_concept(phekb, self.detail)
            logger.info("PHEKB concept file Created Successfully...")
            save_concept(PHEKB_DIR,self.concept,'PHEKB')
        except:
            logger.exception("ERROR while creating PHEKB concept file")
