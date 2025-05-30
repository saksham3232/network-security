import os
import sys
import json
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables from .env file
load_dotenv()

# Retrieve MongoDB URL from environment variables
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class NetworkDataExtract:
    def __init__(self):
        try:
            # Initialize MongoDB client with TLS/SSL configuration
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=certifi.where()
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_convertor(self, file_path):
        try:
            # Read CSV file into DataFrame
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # Convert DataFrame to list of JSON records
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            # Access specified database and collection
            db = self.mongo_client[database]
            coll = db[collection]
            # Insert records into collection
            coll.insert_many(records)
            return len(records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    FILE_PATH = "Network_Data\\phisingData.csv"
    DATABASE = "SAKSHAM"
    COLLECTION = "NetworkData"
    try:
        network_obj = NetworkDataExtract()
        records = network_obj.csv_to_json_convertor(file_path=FILE_PATH)
        print(records)
        no_of_records = network_obj.insert_data_mongodb(records, DATABASE, COLLECTION)
        print(f"{no_of_records} records inserted successfully.")
    except NetworkSecurityException as e:
        logging.error(f"An error occurred: {e}")