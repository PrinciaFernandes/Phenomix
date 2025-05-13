from src.utils import save_json,save_concept,save_detail
from src.config import RAW_DIR,CPRD_URL,CPRD_DIR

from src.scraping.cprd_webscrapping import cprd_scrapping
from src.processing.cprd_concept_detail import get_detail,get_concept
from src.logger import get_logger

logger = get_logger(__name__)

class CPRDPipeline:

    def __init__(self):
        self.detail = None
        self.concept = None

    def main(self):
        try:
            logger.info("SCRAPPING CPRD phenotypes...")
            base_url = CPRD_URL
            cprd = cprd_scrapping(base_url)
            logger.info("SCRAPPING CPRD done successfully")
            save_json(RAW_DIR,cprd,'CPRD')
        except:
            logger.exception("ERROR while scrapping CPRD phenotypes")

        try:
            logger.info("Creating CPRD detail file...")
            self.detail = get_detail(cprd)
            logger.info("CPRD detail file Created Successfully...")
            save_detail(CPRD_DIR,self.detail,'CPRD')
        except:
           logger.exception("ERROR while creating CPRD detail file")            

        try:
            logger.info("Creating CPRD concept file...")
            self.concept = get_concept(cprd,self.detail)
            logger.info("CPRD concept file Created Successfully...")
            save_concept(CPRD_DIR,self.concept,'CPRD')
        except:
            logger.exception("ERROR while creating CPRD concept file")