from src.entity.configuration_entity import ModelHyperparameterConfig,ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainingArtifact,DataTransformationArtifact,ModelHyperparameterArtifact
from src.utils import get_input_data
from sklearn.model_selection import train_test_split
from src.utils import read_yaml,store_model,upload_file
from src.logger import logging
from sklearn.model_selection import  RandomizedSearchCV
from sklearn.metrics import f1_score
from src.exception import CustomException
from sklearn.model_selection import StratifiedKFold
import sys
import numpy as np
from src.config.database.mongodb_config import MongoDB
from datetime import datetime

class ModelHyperparamterTuning:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact, model_trainer_config:ModelTrainerConfig,
                 model_tuning_config:ModelHyperparameterConfig):
        
        self.model_tuning_config  = model_tuning_config
        # self.model_training_artifact = model_training_artifact
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact
        
        self.X,self.y = get_input_data(self.data_transformation_artifact.train_feature_path,
                                         self.data_transformation_artifact.test_feature_path)    
        self.X_train,self.X_test,self.y_train,self.y_test = train_test_split(self.X,self.y,test_size=  0.20)    


    def start_searching_parameters(self,model,params):
        try:
            logging.info("starting random search for best parameter")
            randomsearchcv = RandomizedSearchCV(estimator = model, param_distributions=params,
                                                scoring="f1",cv = 10,verbose=20,n_jobs = -1)
            randomsearchcv.fit(self.X_train,self.y_train)
            logging.info("randomsearchcv best estimator score")
            pred_training = randomsearchcv.best_estimator_.predict(self.X_train)
            logging.info(f"training score: {f1_score(pred_training,self.y_train)}")
            pred_testing = randomsearchcv.best_estimator_.predict(self.X_test)
            logging.info(f"training score: {f1_score(pred_testing,self.y_test)}")
            logging.info("completed random search for best parameter")
            return randomsearchcv.best_params_
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)

    
    def test_model(self,model):
        try:
            model_f1_score_testing = []
            model_f1_score_training = []
            logging.info(f"training {model}")
            
            stratified_k_fold = StratifiedKFold(n_splits= 10,shuffle=True,random_state=42)
            for train_index, test_index in stratified_k_fold.split(self.X, self.y):
                X_train,X_test = self.X[train_index],self.X[test_index]
                y_train,y_test = self.y[train_index],self.y[test_index]
                
                model.fit(X = X_train,y = y_train)
                pred = model.predict(X_train)
                model_f1_score_training.append(f1_score(y_train,pred))
                y_pred = model.predict(X_test)
                model_f1_score_testing.append(f1_score(y_test,y_pred))

            logging.info(f"training score: {np.mean(model_f1_score_training)}")
            logging.info(f"testing score: {np.mean(model_f1_score_testing)}")
            
            store_model(model,self.model_tuning_config.model_path)
            upload_file(self.model_tuning_config.model_path,self.model_tuning_config.s3_bucket_name,self.model_tuning_config.model_s3_path)

            return np.mean(model_f1_score_training),np.mean(model_f1_score_testing)
        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)
    

    def fine_tune_model(self):
        try:
            logging.info("searching best parameter for model")
            model = list(self.model_trainer_config.model_config.keys())[0]
            model_params = read_yaml(self.model_tuning_config.model_parameter)['model']
            best_param = self.start_searching_parameters(self.model_trainer_config.model_config[model], model_params[model])
            logging.info("testing model with best parameter")
            trained_score,test_score = self.test_model(self.model_trainer_config.model_config[model].set_params(**best_param))
            mongodb_obj = MongoDB()
            now = int(datetime.now().timestamp())
            metrics_json = {'model': model,
                            'model_best_params':best_param,
                            'f1_training':trained_score,
                            'fl_testing':test_score 
                            }
            mongodb_obj.write_data(
            {"timestamp": now,
                "report": metrics_json}
                ,self.model_tuning_config.model_tune_collection)

            model_tuning_artifact = ModelHyperparameterArtifact(
                model_path= self.model_tuning_config.model_path,
                tuning_status=True
            )
            return model_tuning_artifact

        except Exception as e:
            logging.exception(e)
            raise CustomException(e,sys)
