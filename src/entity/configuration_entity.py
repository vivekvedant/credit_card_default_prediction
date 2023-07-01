from dataclasses import dataclass
import os
from src.constant.training_pipeline import (
    ROOT_DIR,ARTIFACT_DIR,PROCESSED_DATA_DIR,TRAIN_DATA_FILENAME,TEST_DATA_FILENAME,
    RAW_DATA_DIR,RAW_DATA_FILENAME,S3_BUCKET_NAME,VALID_DATA_DIR,INVALID_DATA_DIR,
    SCHEMA_FILENAME,DRIFT_REPORT_COLLECTION,PREPROSSED_PKL,CONFIG_DIR,
    CATEGORY_ENCODING_FILE_PATH,TRANSFORMED_FEATURE_DIR,TRANSFORMED_TRAIN_FEATURE,
    TRANSFORMED_TEST_FEATURE,MODEL_REPORT_COLLECTION,MODEL_DIR,MODEL_FILE_NAME,MODEL_PARAMERTER,
    MODEL_TUNE_REPORT_COLLECTION

)
from src.config.model_config import model_config



@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,PROCESSED_DATA_DIR,TRAIN_DATA_FILENAME)
    train_data_s3_path = f"{PROCESSED_DATA_DIR}/{TRAIN_DATA_FILENAME}"

    test_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,PROCESSED_DATA_DIR,TEST_DATA_FILENAME)
    test_data_s3_path = f"{PROCESSED_DATA_DIR}/{TEST_DATA_FILENAME}"
    
    raw_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,RAW_DATA_DIR,RAW_DATA_FILENAME)

    raw_data_s3_path = f"{RAW_DATA_DIR}/{RAW_DATA_FILENAME}"

    s3_bucket_name = S3_BUCKET_NAME


@dataclass
class DataValidationConfig:
    train_valid_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,VALID_DATA_DIR,TRAIN_DATA_FILENAME)
    train_valid_data_s3_path = f"{VALID_DATA_DIR}/{TRAIN_DATA_FILENAME}"
    
    test_valid_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,VALID_DATA_DIR,TEST_DATA_FILENAME)
    test_valid_data_s3_path = f"{VALID_DATA_DIR}/{TEST_DATA_FILENAME}"
    
    train_invalid_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,INVALID_DATA_DIR,TRAIN_DATA_FILENAME)
    train_invalid_data_s3_path = f"{INVALID_DATA_DIR}/{TRAIN_DATA_FILENAME}"

    test_invalid_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,INVALID_DATA_DIR,TEST_DATA_FILENAME)
    test_invalid_data_s3_path = f"{INVALID_DATA_DIR}/{TEST_DATA_FILENAME}"

    data_schema = os.path.join(ROOT_DIR,ARTIFACT_DIR,SCHEMA_FILENAME)

    mongodb_collection_drift_report = DRIFT_REPORT_COLLECTION

    s3_bucket_name = S3_BUCKET_NAME



@dataclass
class DataTransformationConfig:
    processed_data_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,PREPROSSED_PKL)
    processed_data_s3_path = f"{PREPROSSED_PKL}"

    categorical_encoding_yaml = os.path.join(ROOT_DIR,CONFIG_DIR,CATEGORY_ENCODING_FILE_PATH)
    categorical_encoding_yaml_s3_path = f"{CONFIG_DIR}/{CATEGORY_ENCODING_FILE_PATH}"

    train_array_file_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,TRANSFORMED_FEATURE_DIR,TRANSFORMED_TRAIN_FEATURE)
    train_array_file_path_s3_path = f"{TRANSFORMED_FEATURE_DIR}/{TRANSFORMED_TRAIN_FEATURE}"

    test_array_file_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,TRANSFORMED_FEATURE_DIR,TRANSFORMED_TEST_FEATURE)
    test_array_file_path_s3_path = f"{TRANSFORMED_FEATURE_DIR}/{TRANSFORMED_TEST_FEATURE}"

    s3_bucket_name = S3_BUCKET_NAME

@dataclass
class ModelTrainerConfig:
    model_config = model_config
    model_report = MODEL_REPORT_COLLECTION


@dataclass
class ModelHyperparameterConfig:
    model_config = model_config
    
    model_path = os.path.join(ROOT_DIR,ARTIFACT_DIR,MODEL_DIR,MODEL_FILE_NAME)
    model_s3_path = f"{MODEL_DIR}/{MODEL_FILE_NAME}"

    model_parameter = os.path.join(ROOT_DIR,CONFIG_DIR,MODEL_PARAMERTER)
    model_tune_collection = MODEL_TUNE_REPORT_COLLECTION
    s3_bucket_name = S3_BUCKET_NAME