import json
import os
from src.masterlist.masterlist import transform_detail,create_masterlist
from src.pipeline.sentinel_pipe import SentinalPipeline
from src.pipeline.hdruk_pipe import HDRUKPipeline
from src.pipeline.cprd_pipe import CPRDPipeline
from src.pipeline.phekb_pipe import PHEKBPipeline
from src.pipeline.ohdsi_pipe import OHDSIPipeline
from src.config import MASTERLIST_DIR
from src.database.neo4j import push_to_neo4j
from src.logger import get_logger

logger = get_logger(__name__)

detail_files = []
concept_files = []
logger.info("STARTING PIPELINE...")

#----------------------------------------------------------SENTINEL_PIPELINE------------------------------------------------------------------------
try:
    logger.info("STARTING SENTINEL PIPELINE...")
    sentinal_obj = SentinalPipeline()
    sentinal_obj.main()
    logger.info("SENTINEL PIPELINE COMPLETED SUCCESSFULLY")
    detail_files.extend(sentinal_obj.detail)
    concept_files.extend(sentinal_obj.concept)
    logger.debug(f"SENTINEL DETAIL FILE APPENDED")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE SENTINEL PIPELINE")


#----------------------------------------------------------HDRUK_PIPELINE-------------------------------------------------------------------------
try:
    logger.info("STARTING HDRUK PIPELINE...")
    hdruk_obj = HDRUKPipeline()
    hdruk_obj.main()
    logger.info("HDRUK PIPELINE COMPLETED SUCCESSFULLY")
    detail_files.extend(hdruk_obj.detail)
    concept_files.extend(hdruk_obj.concept)
    logger.debug(f"HDRUK DETAIL FILE APPENDED")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE HDRUK PIPELINE")


#----------------------------------------------------------CPRD_PIPELINE---------------------------------------------------------------------------
try:
    logger.info("STARTING CPRD PIPELINE...")
    cprd_obj = CPRDPipeline()
    cprd_obj.main()
    logger.info("CPRD PIPELINE COMPLETED SUCCESSFULLY")
    detail_files.extend(cprd_obj.detail)
    concept_files.extend(cprd_obj.concept)
    logger.debug(f"CPRD DETAIL FILE APPENDED")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE CPRD PIPELINE")    


#----------------------------------------------------------PHEKB_PIPELINE-------------------------------------------------------------------------
try:
    logger.info("STARTING PHEKB PIPELINE...")
    phekb_obj = PHEKBPipeline()
    phekb_obj.main()
    logger.info("PHEKB PIPELINE COMPLETED SUCCESSFULLY")
    detail_files.extend(phekb_obj.detail)
    concept_files.extend(phekb_obj.concept)
    logger.debug(f"PHEKB DETAIL FILE APPENDED")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE PHEKB PIPELINE")  

#----------------------------------------------------------OHDSI_PIPELINE-------------------------------------------------------------------------
try:
    logger.info("STARTING OHDSI PIPELINE...")
    ohdsi_obj = OHDSIPipeline()
    ohdsi_obj.main()
    logger.info("OHDSI PIPELINE COMPLETED SUCCESSFULLY")
    detail_files.extend(ohdsi_obj.detail)
    concept_files.extend(ohdsi_obj.concept)
    logger.debug(f"OHDSI DETAIL FILE APPENDED")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE OHDSI PIPELINE")  

#----------------------------------------------------------MASTERLIST---------------------------------------------------------------------------
try:
    logger.info("CREATING MASTERLIST")
    combined_detail = transform_detail(detail_files)
    masterlist = create_masterlist(combined_detail)
    logger.info("MASTERLIST CREATED SUCCESSFULLY")
    os.makedirs(MASTERLIST_DIR, exist_ok=True)
    with open(rf'{MASTERLIST_DIR}\Masterlist.json','w') as file:
        json.dump(masterlist,file,indent=4)

    logger.debug("MASTERLIST SAVED SUCCESSFULLY")
except:
    logger.exception("AN ERROR OCCURRED WHILE CREATING MASTERLIST ")    

#----------------------------------------------------------NEO4J---------------------------------------------------------------------------
try:
    logger.info("STARTING NEO4J LOADER...")
    push_to_neo4j(masterlist,detail_files,concept_files)
    logger.info("NEO4J LOADING COMPLETED SUCCESSFULLY")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE NEO4J LOADER")

#----------------------------------------------------------END---------------------------------------------------------------------------
