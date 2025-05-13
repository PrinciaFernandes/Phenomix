import json
import os
from src.masterlist.masterlist import transform_detail,create_masterlist
from src.pipeline.sentinel_pipe import SentinalPipeline
from src.pipeline.hdruk_pipe import HDRUKPipeline
from src.pipeline.cprd_pipe import CPRDPipeline
from src.pipeline.phekb_pipe import PHEKBPipeline
from src.pipeline.ohdsi_pipe import OHDSIPipeline
from src.config import MASTERLIST_DIR,PROCESSED_DIR
from src.database.neo4j import push_to_neo4j
from src.logger import get_logger

logger = get_logger(__name__)

# detail_files = []
# concept_files = []
logger.info("STARTING PIPELINE...")

# # #Sentinel
# try:
#     logger.info("STARTING SENTINEL PIPELINE...")
#     sentinal_obj = SentinalPipeline()
#     sentinal_obj.main()
#     logger.info("SENTINEL PIPELINE COMPLETED SUCCESSFULLY")
#     detail_files.extend(sentinal_obj.detail)
#     concept_files.extend(sentinal_obj.concept)
#     logger.debug(f"SENTINEL DETAIL FILE APPENDED")
# except:
#     logger.exception("AN ERROR OCCURRED WHILE RUNNING THE SENTINEL PIPELINE")

# # #HDRUK
# try:
#     logger.info("STARTING HDRUK PIPELINE...")
#     hdruk_obj = HDRUKPipeline()
#     hdruk_obj.main()
#     logger.info("HDRUK PIPELINE COMPLETED SUCCESSFULLY")
#     detail_files.extend(hdruk_obj.detail)
#     concept_files.extend(hdruk_obj.concept)
#     logger.debug(f"HDRUK DETAIL FILE APPENDED")
# except:
#     logger.exception("AN ERROR OCCURRED WHILE RUNNING THE HDRUK PIPELINE")


# # #CPRD
# try:
#     logger.info("STARTING CPRD PIPELINE...")
#     cprd_obj = CPRDPipeline()
#     cprd_obj.main()
#     logger.info("CPRD PIPELINE COMPLETED SUCCESSFULLY")
#     detail_files.extend(cprd_obj.detail)
#     concept_files.extend(cprd_obj.concept)
#     logger.debug(f"CPRD DETAIL FILE APPENDED")
# except:
#     logger.exception("AN ERROR OCCURRED WHILE RUNNING THE CPRD PIPELINE")    


# #PHEKB
# try:
#     logger.info("STARTING PHEKB PIPELINE...")
#     phekb_obj = PHEKBPipeline()
#     phekb_obj.main()
#     logger.info("PHEKB PIPELINE COMPLETED SUCCESSFULLY")
#     # detail_files.extend(phekb_obj.detail)
#     # concept_files.extend(phekb_obj.concept)
#     logger.debug(f"PHEKB DETAIL FILE APPENDED")
# except:
#     logger.exception("AN ERROR OCCURRED WHILE RUNNING THE PHEKB PIPELINE")  

# #OHDSI
# try:
#     logger.info("STARTING OHDSI PIPELINE...")
#     ohdsi_obj = OHDSIPipeline()
#     ohdsi_obj.main()
#     logger.info("OHDSI PIPELINE COMPLETED SUCCESSFULLY")
#     # detail_files.extend(ohdsi_obj.detail)
#     # concept_files.extend(ohdsi_obj.concept)
#     logger.debug(f"OHDSI DETAIL FILE APPENDED")
# except:
#     logger.exception("AN ERROR OCCURRED WHILE RUNNING THE OHDSI PIPELINE")  


def get_detail_files(dir:str)->list:
    logger.info("Extracting detail files")

    detail_files = []
    websites = ['CPRD','HDRUK','OHDSI','PHEKB','SENTINEL']
    for files in os.listdir(dir):
        if files in websites:
            file_path = os.path.join(dir,files)
            for detail in os.listdir(file_path):
                if '_detail.json' in detail:
                    with open(os.path.join(file_path,detail),'r') as f:
                        file_content = f.read()
                    detail_files.extend(json.loads(file_content))
    return detail_files

def get_concept_files(dir:str)->list:
    logger.info("Extracting concept files")

    concept_files = []
    websites = ['CPRD','HDRUK','OHDSI','PHEKB','SENTINEL']
    for files in os.listdir(dir):
        if files in websites:
            file_path = os.path.join(dir,files)
            for detail in os.listdir(file_path):
                if '_concept.json' in detail:
                    with open(os.path.join(file_path,detail),'r') as f:
                        file_content = f.read()
                    concept_files.extend(json.loads(file_content))
    return concept_files

detail_files = get_detail_files(PROCESSED_DIR)
concept_files = get_concept_files(PROCESSED_DIR)

#MASTERLIST
try:
    logger.info("CREATING MASTERLIST")
    combined_detail = transform_detail(detail_files)
    masterlist = create_masterlist(combined_detail)
    logger.info("MASTERLIST CREATED SUCCESSFULLY")
    with open(rf'{MASTERLIST_DIR}\Masterlist.json','w') as file:
        json.dump(masterlist,file,indent=4)

    logger.debug("MASTERLIST SAVED SUCCESSFULLY")
except:
    logger.exception("AN ERROR OCCURRED WHILE CREATING MASTERLIST ")    

#NEO4J
try:
    logger.info("STARTING NEO4J LOADER...")
    push_to_neo4j(masterlist,detail_files,concept_files)
    logger.info("NEO4J LOADING COMPLETED SUCCESSFULLY")
except:
    logger.exception("AN ERROR OCCURRED WHILE RUNNING THE NEO4J LOADER")
