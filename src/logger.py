import logging
import os
from datetime import datetime

# Create 'logs' directory path
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log file with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="%(asctime)s [%(levelname)s] > %(lineno)d | %(filename)s | %(funcName)s | %(message)s",
    level=logging.INFO,
)
console = logging.StreamHandler()
logging.getLogger().addHandler(console)

def get_logger(name=__name__,session_id=None):
    logger = logging.getLogger(name,session_id)
    return logger