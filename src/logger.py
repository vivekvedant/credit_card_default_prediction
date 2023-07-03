import logging
import os
from datetime import datetime
import logging.handlers as handlers
import boto3

logging_str = "[%(asctime)s: %(levelname)s: %(module)s] : %(message)s"
log_dir = "./logs"
current_datetime = datetime.now()
current_date_time = current_datetime.strftime("%m-%d-%Y")
log_file_name = f"running_logs_{current_date_time}.log"
log_filepath = os.path.join(log_dir,log_file_name)
os.makedirs(log_dir,exist_ok=True)
class S3Handler(logging.StreamHandler):
    def __init__(self, s3_client, bucket, key):
        super().__init__()
        self.s3_client = s3_client
        self.bucket = bucket
        self.key = key
        self.log_entries = []

    def emit(self, record):
        try:
            log_entry = self.format(record) + '\n'
            self.log_entries.append(log_entry)
            self.s3_client.put_object(Body=''.join(self.log_entries), Bucket=self.bucket, Key=self.key)
        except Exception as e:
            self.handleError(record)
            msg = f"Failed to write log to S3. Error: {str(e)}"
            self.s3_client.put_object(Body=msg.encode('utf-8'), Bucket=self.bucket, Key=self.key)

s3 = boto3.client('s3')

logging.basicConfig(level=logging.INFO,
                    format=logging_str,
                    handlers=[
                        handlers.TimedRotatingFileHandler(log_filepath,when = "D",interval = 1, 
                                                          backupCount=0),
                        S3Handler(s3, "credit-default-data-versioning", f"logs/{log_file_name}")
                    ])

