import pymongo
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

data = pd.read_csv('test.csv')
print(data)

client = pymongo.MongoClient(os.getenv('MONGO_URI'))

# Specify database
db = client["polilens_data"]
collection = db['test_data']

data_dict = data.to_dict("records")
collection.insert_many(data_dict)

# Check if the database exists
dblist = client.list_database_names()
if "polilens_data" in dblist:
    print("The database exists.")
else:
    print("The database does not exist.")

print(db.list_collection_names())
