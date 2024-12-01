import requests
import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# Preprocess legislator data and store in a DataFrame
def preprocess_legislators_data():
    url = "https://theunitedstates.io/congress-legislators/legislators-current.json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching legislator data: {response.status_code}")
        return pd.DataFrame()
    
    legislators = response.json()
    # Create a DataFrame for easy lookup
    legislator_data = [
        {
            'full_name': f"{legislator['name']['first']} {legislator['name']['last']}".lower(),
            'bioguide_id': legislator.get("id", {}).get("bioguide", None)
        }
        for legislator in legislators
    ]
    return pd.DataFrame(legislator_data)

# Fetches bioguide_id from the preprocessed DataFrame
def fetch_bioguide_id(search_name, legislator_df):
    if search_name == 'N/A' or legislator_df.empty:
        return None
    search_name = search_name.lower()
    match = legislator_df[legislator_df['full_name'].str.contains(search_name)]
    if not match.empty:
        return match.iloc[0]['bioguide_id']
    return None

# Fetches recent trades reported by Congress members
def scrape_and_transform_transactions(legislator_df):
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
            'bioguide': fetch_bioguide_id(trade.get('representative', 'N/A'), legislator_df),
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
    # Preprocess legislator data
    legislator_df = preprocess_legislators_data()
    legislator_df.to_csv('bioguide.csv', index=False)
    print(f"Preprocessed legislator data: {len(legislator_df)} entries")

    # Scrape and transform transactions data
    df_trades = scrape_and_transform_transactions(legislator_df)
    df_trades.to_csv('trades.csv', index=False)
    print("Trade data saved successfully.")