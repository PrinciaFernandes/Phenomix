from src.config import OHDSI_DETAIL_DIR,OHDSI_CONCEPT_DIR,OHDSI_DIR
from src.utils import save_detail,save_concept
from src.processing.ohdsi_concept_detail import get_concept,get_detail,get_ohdsi_data
from src.logger import get_logger

logger = get_logger(__name__)

class OHDSIPipeline:

    def __init__(self):
        self.detail = None
        self.concept = None

    def main(self):
        try:
            logger.info("Creating OHDSI detail file...")
            ohdsi =  get_ohdsi_data(OHDSI_CONCEPT_DIR)
            self.detail = get_detail(OHDSI_DETAIL_DIR)
            logger.info("OHDSI detail file Created Successfully...")
            save_detail(OHDSI_DIR,self.detail,'OHDSI')
        except:
           logger.exception("ERROR while creating OHDSI detail file") 


        try:
            logger.info("Creating OHDSI concept file...")
            self.concept = get_concept(ohdsi,self.detail)            
            logger.info("OHDSI concept file Created Successfully...")
            save_concept(OHDSI_DIR,self.concept,'OHDSI')
        except:
            logger.exception("ERROR while creating OHDSI concept file")