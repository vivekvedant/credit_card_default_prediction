from src.entity.configuration_entity import DataTransformationConfig
from src.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from src.logger import logging
from sklearn.pipeline import Pipeline
from src.components.custom_data_transformer import NumericalTransformer,CategoricalTransformer
from src.exception import CustomException
import sys
import pandas as pd
from imblearn.over_sampling import SMOTE
import numpy as np
from src.utils import write_object,upload_file

class DataTransformation:

    def __init__(self,data_transformation_config: DataTransformationConfig,
                data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        self.dataTransformationConfig = data_transformation_config
        self.data_validation_artifact = data_validation_artifact


    @classmethod
    def feature_transformation(cls):
        try:
            logging.info("Creating pipeline")

            pipeline = Pipeline([
                ("numerical_transformation", NumericalTransformer()),
                ("categorical_transformation", CategoricalTransformer())
            ]
                
            )
            
            logging.info("Pipeline created")

            return pipeline
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)

    
    def  initiate_data_transformation(self):
        try:
            logging.info("reading data")

            train_df = pd.read_parquet(self.data_validation_artifact.train_valid_data_file)
            test_df = pd.read_parquet(self.data_validation_artifact.test_valid_data_file)
            
            logging.info("transforming data")
            processor = DataTransformation.feature_transformation()

            train_df_transformed = processor.fit_transform(train_df)
            test_df_transformed = processor.transform(test_df)

            logging.info("creating input and target features from data")
            input_training_data = train_df_transformed.drop(['ID','target'],axis = 1)
            target_training_data = train_df_transformed['target']

            input_test_data = test_df_transformed.drop(['ID','target'],axis = 1)
            traget_test_data = test_df_transformed['target']
            
            logging.info("applying smote on data")
            smt = SMOTE(random_state=42,sampling_strategy="minority")
            input_train_feature, target_train_feature = smt.fit_resample(input_training_data,target_training_data)
            input_test_feature, target_test_feature = smt.fit_resample(input_test_data,traget_test_data)

            train_arr = np.c_[input_train_feature.to_numpy(),target_train_feature.to_numpy()]
            test_arr = np.c_[input_test_feature.to_numpy(),target_test_feature.to_numpy()]

            write_object(self.dataTransformationConfig.train_array_file_path,train_arr)
            upload_file(self.dataTransformationConfig.train_array_file_path,self.dataTransformationConfig.s3_bucket_name,self.dataTransformationConfig.train_array_file_path_s3_path)

            write_object(self.dataTransformationConfig.test_array_file_path,test_arr)
            upload_file(self.dataTransformationConfig.test_array_file_path,self.dataTransformationConfig.s3_bucket_name,self.dataTransformationConfig.test_array_file_path_s3_path)

            write_object(self.dataTransformationConfig.processed_data_path,processor)
            upload_file(self.dataTransformationConfig.processed_data_path,self.dataTransformationConfig.s3_bucket_name,self.dataTransformationConfig.processed_data_s3_path)

            data_transformation_artifact = DataTransformationArtifact(
                train_feature_path=self.dataTransformationConfig.train_array_file_path,
                test_feature_path=self.dataTransformationConfig.test_array_file_path,
                processed_pipeline_path=self.dataTransformationConfig.processed_data_path
            )

            return data_transformation_artifact
        
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)