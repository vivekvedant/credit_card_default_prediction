from fastapi import FastAPI,Depends
from fastapi.responses import Response
from src.pipeline.training_pipeline import TrainingPipeline
from fastapi.middleware.cors import CORSMiddleware
from src.pipeline.prediction_pipeline import PredictionPipeline
from src.prediction_params import PredictionParams
from fastapi import File, UploadFile
from src.utils import upload_file
from src.constant.training_pipeline import (
     RAW_DATA_FILENAME,RAW_DATA_DIR,S3_BUCKET_NAME
)
from src.entity.configuration_entity import DataIngestionConfig

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload_data")
async def upload_data(file: UploadFile = File(...)):
    try:
        file.file.seek(0)
        dest_path = DataIngestionConfig.raw_data_s3_path
        upload_file(file.file, S3_BUCKET_NAME,dest_path,file_object= True)
        return Response("Data uploaded successfully")
    except Exception as e:
        return Response(e)
    finally:
        file.file.close()

@app.get("/train/")
async def train_model():
       try:
            training_pipeline = TrainingPipeline()
            training_pipeline.run_training_pipeline()
            return Response("Training completed successfully")
       except Exception as e:
            return Response(e)
    

@app.get("/predict")
async def get_prediction(data: PredictionParams = Depends(PredictionParams)):
      try:
          prediction_pipeline = PredictionPipeline()
          prediction_values = data.to_dict()
          return f"Predicted Value: {prediction_pipeline.predict(prediction_values)}"
      except Exception as e:
          return Response(e)