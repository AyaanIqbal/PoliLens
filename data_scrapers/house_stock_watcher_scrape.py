import requests
import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

def fetch_bioguide_id(search_name):
    # Fetch the JSON data from the URL
    url = "https://theunitedstates.io/congress-legislators/legislators-current.json"
    response = requests.get(url)
    legislators = response.json()

    if search_name == 'N/A':
        return None

    # Search for the legislator
    for legislator in legislators:
        full_name = f"{legislator['name']['first']} {legislator['name']['last']}"
        if search_name.lower() in full_name.lower():
            bioguide_id = legislator.get("id", {}).get("bioguide")
            return bioguide_id

    # If no matches are found, return None
    return None

# Fetches recent trades reported by Congress members
def scrape_and_transform_transactions():
    BASE_URL = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"

    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

    data = response.json()

    # Data mapping
    transaction_type = {
        'exchange' : 'purchase', 
        'purchase' : 'purchase', 
        'sale_full' : 'sale_full',
        'sale_partial' : 'sale_partial'
    }

    # Process transactions into structured data
    trade_list = []
    for trade in tqdm(data, desc="Processing trades"):
        trade_info = {
            'ticker': trade.get('ticker', 'N/A'),
            'representative': trade.get('representative', 'N/A'),
            'bioguide': fetch_bioguide_id(trade.get('representative', 'N/A')),
            'transaction_date': trade.get('transaction_date', 'N/A'),
            'disclosure_date': trade.get('disclosure_date', 'N/A'),
            'amount': trade.get('amount', 'N/A'),
            'transaction_type': transaction_type.get(trade.get('type', 'N/A'), 'N/A'),
            'party': trade.get('party', 'N/A'),
            'sector': trade.get('sector', 'N/A')
        }
        trade_list.append(trade_info)

    # Convert to DataFrame and handle date columns
    df = pd.DataFrame(trade_list)

    # Filter out trades with ticker "--"
    df = df[df['ticker'] != '--']

    # Convert 'transaction_date' and 'disclosure_date' to datetime, filter invalid dates
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df['disclosure_date'] = pd.to_datetime(df['disclosure_date'], errors='coerce')
    df = df[df['transaction_date'].notna() & df['disclosure_date'].notna()]

    return df

# Main script (For Test)
if __name__ == "__main__":
    # Scrape and transform transactions data
    df_trades = scrape_and_transform_transactions()
    df_trades.to_csv('trades.csv', index=False)
    print("Trade data saved successfully.")