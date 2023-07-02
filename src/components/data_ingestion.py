import os
from sklearn.model_selection import train_test_split
from src.logger import logging
from src.exception import CustomException
import sys
import pandas as pd
from src.entity.configuration_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.utils import upload_file,read_csv

class DataIngestion:

    def __init__(self,data_ingestion_config: DataIngestionConfig) -> DataIngestionArtifact:
        self.data_ingestion_config = data_ingestion_config

    
    def initiate_dataIngestion(self):
        try:
            logging.info("Initiate DataIngestion")
            raw_data = pd.read_excel(read_csv(self.data_ingestion_config.raw_data_s3_path,
                                              self.data_ingestion_config.s3_bucket_name),
                                              header = 1)

            raw_data = raw_data.rename(columns = {"default payment next month":"target"})

            train_data,test_data = train_test_split(raw_data,test_size=0.2,random_state=42)

            logging.info("Saving splitted data")

            train_data.to_parquet(self.data_ingestion_config.train_data_path,index = False)
            test_data.to_parquet(self.data_ingestion_config.test_data_path,index = False)

            logging.info("Storing data files in s3")
            upload_file(self.data_ingestion_config.train_data_path,
                        self.data_ingestion_config.s3_bucket_name,
                        self.data_ingestion_config.train_data_s3_path)
            
            upload_file(self.data_ingestion_config.train_data_path,
                        self.data_ingestion_config.s3_bucket_name,
                        self.data_ingestion_config.test_data_s3_path)

                             
            
            logging.info("Completed DataIngestion")

            data_ingestion_artifact = DataIngestionArtifact(train_data_path = self.data_ingestion_config.train_data_path,
                                                            test_data_path = self.data_ingestion_config.test_data_path)
            return data_ingestion_artifact
        
        except Exception as e:
            logging.exception(e)
            raise CustomException(e ,sys)

