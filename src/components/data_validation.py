
from src.entity.configuration_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from src.utils import read_yaml
from src.logger import logging
import json
from src.exception import CustomException
import sys
from src.config.database.mongodb_config import MongoDB
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from datetime import datetime
import shutil
from src.utils import upload_file
import pandas as pd

class DataValidation:
    def __init__(self,data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.schema = read_yaml(self.data_validation_config.data_schema)


    def validate_columns(self,df,type):
        try:
            status = True
            if type == 'numerical':
                cols_from_schema = self.schema['numerical']
            else:
                cols_from_schema = self.schema['categorical']

            report = {'missing_columns': [],"different_datatype":[]}
            for col in cols_from_schema:
                if col in list(df.columns):
                    if cols_from_schema[col]['type'] != df[col].dtype.name:
                        report['missing_columns'].append(col)
                else:
                    report['different_datatype'].append(col)

            if len(report['missing_columns']) > 0:
                status = False
                logging.error(f"{report['missing_columns']} columns are missing in dataset")
                
            if len(report['different_datatype']) > 0:
                   status = False
                   logging.error(f"{json['different_datatype']} have different datatype in testing dataset")
                   
            return status

        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)


    def data_drift(self,df1,df2):
        try:
            mongodb_obj = MongoDB()
            status = True
            logging.info("Starting data drift")
            report = Report(metrics=[ DataDriftPreset()])
            report.run(reference_data=df1, current_data=df2)
            report_json = json.loads(report.json())
            report_json['timestamp'] = int(datetime.strptime(report_json['timestamp'].split(".")[0],"%Y-%m-%d %H:%M:%S").timestamp())
            mongodb_obj.write_data(report_json,self.data_validation_config.mongodb_collection_drift_report)
            if report_json['metrics'][0]['result']['dataset_drift']:
                detected_drif_columns = report_json['metrics'][0]['result']['number_of_drifted_columns']
                status= False
                logging.error("Data Drift is detected in {}".format(detected_drif_columns))

            return status
        
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)


    def initiate_data_validation(self):
        try:
            logging.info("reading raw data")
            train_data = pd.read_parquet(self.data_ingestion_artifact.train_data_path)
            test_data = pd.read_parquet(self.data_ingestion_artifact.test_data_path)

            number_of_cols = len(self.schema['categorical']) + len(self.schema['numerical']) + len(self.schema['target']) 
            training_status = True
            test_status = True
            validation_status = True

            if train_data.shape[1] != number_of_cols:
                training_status = False
                logging.error("There is additional column in the training dataset") 
            
            if test_data.shape[1] != number_of_cols:
                test_status = False
                logging.error("There is additional column in the test dataset") 
            
            training_status = self.validate_columns(train_data,type = 'numerical')

            test_status = self.validate_columns(test_data,type = 'numerical')

            training_status = self.validate_columns(train_data,type = 'categorical')

            test_status = self.validate_columns(test_data,type = 'categorical')

            status = self.data_drift(train_data,test_data)

            if status and training_status:
                shutil.copy(self.data_ingestion_artifact.train_data_path,self.data_validation_config.train_valid_data_path)
                upload_file(self.data_validation_config.train_valid_data_path,self.data_validation_config.s3_bucket_name,self.data_validation_config.train_valid_data_s3_path)
                
            else:
                shutil.copy(self.data_ingestion_artifact.train_data_path,self.data_validation_config.train_invalid_data_path)
                upload_file(self.data_validation_config.train_invalid_data_path,self.data_validation_config.s3_bucket_name,self.data_validation_config.train_invalid_data_s3_path)
            
            if status and  test_status:
                shutil.copy(self.data_ingestion_artifact.train_data_path,self.data_validation_config.test_valid_data_path)
                upload_file(self.data_validation_config.test_valid_data_path,self.data_validation_config.s3_bucket_name,self.data_validation_config.test_valid_data_s3_path)

            else:
                shutil.copy(self.data_ingestion_artifact.train_data_path,self.data_validation_config.test_invalid_data_path)
                upload_file(self.data_validation_config.test_invalid_data_path,self.data_validation_config.s3_bucket_name,self.data_validation_config.test_invalid_data_s3_path)

            if not training_status or not test_status or  not status:
                validation_status = False
            
            if not validation_status:
                raise Exception

            data_validation_artifacts = DataValidationArtifact(
                train_invaild_data_file=self.data_validation_config.train_valid_data_path,
                test_invalid_data_file=self.data_validation_config.test_invalid_data_path,
                train_valid_data_file=self.data_validation_config.train_valid_data_path,
                test_valid_data_file=self.data_validation_config.test_valid_data_path
            )

            return data_validation_artifacts


        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)