# In this file we will query the data from database to make sure we have added data.
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load Mongo URI From env
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

# Accessing job_candidates
db = client[db_name]
collections = db.list_collection_names()
print("Collections in '{}':".format(db_name), collections)

def list_all_documents(connection_string, db_name, collection_name):
    client = MongoClient(connection_string)
    db = client[db_name]
    collection = db[collection_name]

    documents = collection.find()
    for doc in documents:
        print(doc)

if __name__ == "__main__":
    connection_string = MONGO_URI
    db_name = 'job_candidates'
    collection_name = 'candidates'

    print("\nListing all data in the collection:")
    list_all_documents(connection_string, db_name, collection_name)
