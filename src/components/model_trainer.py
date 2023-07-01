from src.logger import logging
from src.entity.configuration_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainingArtifact,DataTransformationArtifact
import pandas as pd
from src.utils import get_input_data
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score
import numpy as np
from src.exception import CustomException
from src.config.database.mongodb_config import MongoDB
import sys
from datetime import datetime
from joblib import Parallel, delayed
from src.constant.training_pipeline import NO_PARALLEL_JOBS

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        self.models = self.model_trainer_config.model_config

    def train_model(self,model):
        try:
           
            X, y = get_input_data(self.data_transformation_artifact.train_feature_path,self.data_transformation_artifact.test_feature_path)
            
            stratified_k_fold = StratifiedKFold(n_splits= 10,shuffle=True,random_state=42)

            model_f1_score_testing = []
            model_f1_score_training = []
            logging.info(f"training {model}")
            model_obj =  self.models[model]
            for train_index, test_index in stratified_k_fold.split(X, y):
                X_train,X_test = X[train_index],X[test_index]
                y_train,y_test = y[train_index],y[test_index]
                model_obj.fit(X = X_train,y = y_train)
                pred = model_obj.predict(X_train)
                model_f1_score_training.append(f1_score(y_train,pred))
                y_pred = model_obj.predict(X_test)
                model_f1_score_testing.append(f1_score(y_test,y_pred))
            logging.info(f"model: {model} | training_score: {np.mean(model_f1_score_training)} | testing_score:  {np.mean(model_f1_score_testing)}|")
            
            metrics_json = {'model':model,'f1_training':np.mean(model_f1_score_training),
                    'fl_testing':np.mean(model_f1_score_testing) 
            }
            
            return metrics_json
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)
    
    def initiate_model_training(self):
        mongodb_obj = MongoDB()
        
        now = int(datetime.now().timestamp())
        model_result_dict_list = []
        model_result_dict  = Parallel(n_jobs=NO_PARALLEL_JOBS)(delayed(self.train_model)(model) for model in self.models.keys())
        print(model_result_dict)
        model_result_dict_list.append(model_result_dict)
        
        mongodb_obj.write_data(
                {"timestamp": now,
                 "report": model_result_dict_list}
                 ,self.model_trainer_config.model_report)
        model_training_artifact = ModelTrainingArtifact(model_training_summary= pd.DataFrame(model_result_dict_list))
        
        return  model_training_artifact
