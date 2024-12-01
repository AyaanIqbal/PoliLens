import pymongo
import pandas as pd
import os
from dotenv import load_dotenv
from data_scrapers import bills_data as bd, house_stock_watcher_scrape as td 

# Load environment variables
load_dotenv()

# Connect to MongoDB
client = pymongo.MongoClient(os.getenv('MONGO_URI'))

# Call scraping functions for trades and bills
trade_df = td.scrape_and_transform_transactions()
bill_df = bd.fetch_bills(116, 'HR')
congress_df = bd.fetch_congress_members(116)

# Specify database and collections
db = client["polilens_data"]
trade_collection = db['trades']
bill_collection = db['bills']
congress_collection = db['congress-members']

# Convert trade, bills, congress members DataFrame to dictionary for MongoDB insertion
trade_data_dict = trade_df.to_dict("records")
bill_data_dict = bill_df.to_dict("records")
congress_data_dict = congress_df.to_dict("records")

# Insert trade data into MongoDB collection
try:
    trade_collection.insert_many(trade_data_dict)
    print("Trade data successfully inserted into MongoDB.")
except Exception as e:
    print(f"An error occurred while inserting trade data: {e}")

# Insert bill data into MongoDB collection
try:
    bill_collection.insert_many(bill_data_dict)
    print("Bill data successfully inserted into MongoDB.")
except Exception as e:
    print(f"An error occurred while inserting bill data: {e}")

# Insert congress data into MongoDB collection
try:
    congress_collection.insert_many(congress_data_dict)
    print("Congress data successfully inserted into MongoDB.")
except Exception as e:
    print(f"An error occurred while inserting congress data: {e}")

# Check if the database exists
dblist = client.list_database_names()
if "polilens_data" in dblist:
    print("The database exists.")
else:
    print("The database does not exist.")

# Print the list of collections in the database
print(db.list_collection_names())
