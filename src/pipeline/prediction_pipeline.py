
from src.entity.configuration_entity import PredictionPipelineConfig
from src.utils import read_object
from src.logger import logging
from src.exception import CustomException
import sys
from src.utils import read_yaml
import pandas as pd
from src.utils import load_model

class PredictionPipeline:
    def __init__(self):
        self.pipelineConfig = PredictionPipelineConfig()

    def transform_data(self, data):
        try:
            processor = read_object(self.pipelineConfig.processed_data_path)
            return processor.transform(data)
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)
    
    def reverse_encoding(self,data):
         categorical_yaml = read_yaml(self.pipelineConfig.schema_encoding_yaml)['categorical']
         categorical_encoding_yaml = read_yaml(self.pipelineConfig.categorical_encoding_yaml)
         for col in categorical_yaml.keys():
            inv_categorical_yaml = {v: k for k, v in categorical_encoding_yaml[col].items()}
            data[col] = inv_categorical_yaml[data[col].value.split(' ')[0]]
         return data


    def predict(self,data):
        try:
            logging.info("reverse encoding")
            data = self.reverse_encoding(data)
            logging.info("transform data")
            transformed_data = self.transform_data(pd.DataFrame([data]))
            
            logging.info("complted transforming the data")
            
            logging.info("loading model")
            model = load_model(self.pipelineConfig.model_path)
            logging.info("completed loading model")
            
            return int(model.predict(transformed_data)[0])
            
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)