# In this program, we will open mongo database, upload candidate data to it under candidates collection
import pandas as pd
from pymongo import MongoClient
import os
from load_dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
db_name = 'job_candidates'
collection_name = 'candidates'

# Connect to MongoDB
client = MongoClient(MONGO_URI)
print(client)

# List all databases
databases = client.list_database_names()
print("Databases:", databases)


db = client[db_name]
collections = db.list_collection_names()
print("Collections in '{}':".format(db_name), collections)


def import_csv_to_mongodb(csv_file_path, connection_string, db_name, collection_name):
    df = pd.read_csv(csv_file_path)

    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    data = df.to_dict(orient='records')
    collection.insert_many(data)

    print(f"Inserted {len(data)} records into the '{collection_name}' collection in the '{db_name}' database.")

if __name__ == "__main__":
    csv_file_path = 'CandidateData.csv'  
    connection_string = MONGO_URI
    db_name = 'job_candidates'
    collection_name = 'candidates'

    import_csv_to_mongodb(csv_file_path, connection_string, db_name, collection_name)

# Success, we have updated 120 records into job_candidates database.