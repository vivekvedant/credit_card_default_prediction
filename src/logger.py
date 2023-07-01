import logging
import os
from datetime import datetime
import logging.handlers as handlers


logging_str = "[%(asctime)s: %(levelname)s: %(module)s] : %(message)s"
log_dir = "./logs"
current_datetime = datetime.now()
current_date_time = current_datetime.strftime("%m-%d-%Y")
log_filepath = os.path.join(log_dir,f"running_logs_{current_date_time}.log")
os.makedirs(log_dir,exist_ok=True)


logging.basicConfig(level=logging.INFO,
                    format=logging_str,
                    handlers=[
                        handlers.TimedRotatingFileHandler(log_filepath,when = "D",interval = 1, 
                                                          backupCount=0)
                    ])

