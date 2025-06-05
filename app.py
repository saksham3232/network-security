import sys
import os
import pandas as pd
import certifi
import pymongo
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(f"MongoDB URL: {mongo_db_url}")

# MongoDB Setup
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

# Access database and collection
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI App
app = FastAPI()
origins = "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Templates
templates = Jinja2Templates(directory="templates")

# Custom modules
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# Root route
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# Train model endpoint
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training pipeline executed successfully.")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Prediction endpoint
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # Load preprocessor and model
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

        print(df.iloc[0])

        # Make prediction
        y_pred = network_model.predict(df)
        print(y_pred)

        df["predicted_column"] = y_pred
        print(df["predicted_column"])
        

        # Save prediction
        output_path = "prediction_output/output.csv"
        df.to_csv(output_path, index=False)
        print(df["predicted_column"])

        table_html = df.to_html(classes="table table-striped", index=False)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Shutdown event to close MongoDB connection
@app.on_event("shutdown")
def shutdown_event():
    client.close()

# Run app with uvicorn
if __name__ == "__main__":
    app_run("app:app", host="0.0.0.0", port=8000, reload=True)
