from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_hyperparameter_tuning import ModelHyperparamterTuning
from src.entity.configuration_entity import(
     DataIngestionConfig,DataValidationConfig,DataTransformationConfig,
     ModelTrainerConfig,ModelHyperparameterConfig
)
from src.entity.artifact_entity import(
    DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
)
from src.components.data_validation import DataValidation
from src.logger import logging
from src.exception import CustomException
import sys



class TrainingPipeline:
    def __init__(self):
         self.data_ingestion_config = DataIngestionConfig()
         self.data_validation_config = DataValidationConfig()
         self.data_transformation_config =  DataTransformationConfig()
         self.model_training_config = ModelTrainerConfig()
         self.mode_hyperparameter_config = ModelHyperparameterConfig()
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("starting dataIngestion")
            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_dataIngestion()
            logging.info("completed Data Ingestion")
            return data_ingestion_artifact
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            logging.info("starting data validation")
            data_validation = DataValidation(self.data_validation_config,data_ingestion_artifact)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("completed data validation")
            return data_validation_artifact
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            logging.info("starting data transformation")
            data_transformation = DataTransformation(self.data_transformation_config,data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("completed Data Transformation")
            return data_transformation_artifact
            
        except Exception as e:
            logging.info(e)
            raise CustomException(e, sys)
        
    def start_training(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("starting training")
            model_training = ModelTrainer(self.model_training_config,data_transformation_artifact)
            model_training_artifact = model_training.initiate_model_training()
            logging.info("completed model training")
            return model_training_artifact

        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    def start_model_tuning(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            
            logging.info("starting model tuning")
            model_hyper_parameter_tuning = ModelHyperparamterTuning(data_transformation_artifact,self.model_training_config,
                                                                    self.mode_hyperparameter_config)
            model_hyper_parameter_tuning.fine_tune_model()
            logging.info("completed model tuning")
        except Exception as e:
            logging.exception(e)
            raise CustomException(e, sys)
        
    
    def run_training_pipeline(self):
        logging.info("starting training pipeline")

        data_ingestion_artifacts = self.start_data_ingestion()

        data_validation_artifacts = self.start_data_validation(data_ingestion_artifacts)

        data_transformation_artifacts = self.start_data_transformation(data_validation_artifacts)

        model_training = self.start_training(data_transformation_artifacts)
        model_tuning = self.start_model_tuning(data_transformation_artifacts)

        logging.info("completed training pipeline")


if __name__ == "__main__":
    training_pipeine = TrainingPipeline()
    training_pipeine.run_training_pipeline()