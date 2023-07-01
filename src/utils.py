import os
from src.logger import logging
from src.exception import CustomException
import sys
import boto3
import io
import pickle
import yaml
import numpy as np
import joblib

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
    


def read_csv(file_name,bucket):
    s3_client = boto3.client('s3')
    try:
        csv_obj = s3_client.get_object(Bucket = bucket, Key = file_name)
        return io.BytesIO(csv_obj['Body'].read())
    except Exception as e:
        raise CustomException(e, sys)
    

def write_object(filename,content):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(content,f)
    except Exception as e:
        logging.exception(e)
        raise CustomException(e,sys)
    

def read_yaml(file_name):
    try:
        with open(file_name) as f:
            my_dict = yaml.safe_load(f)

        return my_dict
    
    except Exception as e:
        logging.exception(e)
        raise CustomException(e,sys)
    
def read_object(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logging.exception(e)
        raise CustomException(e,sys)
    


def get_input_data(train_feature_path,test_feature_path):
    X = np.concatenate([read_object(train_feature_path)[:,:-1], 
                        read_object(train_feature_path)[:,:-1]])

    y = np.concatenate([read_object(test_feature_path)[:,-1],
                        read_object(test_feature_path)[:,-1]
                ])
    return X, y

def store_model(content,filename):
    try:
        joblib.dump(content,filename)
    except Exception as e:
        logging.exception(e)
        raise CustomException(e,sys)
    

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except Exception as e:
        logging.error(e)
        raise CustomException(e, sys)
    