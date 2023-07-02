from dataclasses import dataclass
import pandas as pd


@dataclass
class DataIngestionArtifact:
    train_data_path: str
    test_data_path: str

@dataclass
class DataValidationArtifact:
    train_invaild_data_file: str
    test_invalid_data_file: str
    train_valid_data_file: str
    test_valid_data_file: str



@dataclass
class DataTransformationArtifact:
    train_feature_path: str
    test_feature_path: str
    processed_pipeline_path: str


@dataclass
class ModelTrainingArtifact:
    model_training_summary: pd.DataFrame()
