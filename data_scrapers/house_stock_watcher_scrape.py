import requests
import os
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# Fetches recent trades reported by Congress members
def scrape_and_transform_transactions():
    BASE_URL = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"

    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

    data = response.json()

    # Process transactions into structured data
    trade_list = []
    for trade in tqdm(data, desc="Processing trades"):
        trade_info = {
            'ticker': trade.get('ticker', 'N/A'),
            'representative': trade.get('representative', 'N/A'),
            'transaction_date': trade.get('transaction_date', 'N/A'),
            'disclosure_date': trade.get('disclosure_date', 'N/A'),
            'amount': trade.get('amount', 'N/A'),
            'type': trade.get('type', 'N/A'),
            'asset_type': trade.get('asset_type', 'N/A'),
            'district': trade.get('district', 'N/A'),
            'party': trade.get('party', 'N/A')
        }
        trade_list.append(trade_info)

    # Convert to DataFrame and handle date columns
    df = pd.DataFrame(trade_list)

    def safe_to_datetime(val):
        if isinstance(val, str):
            try:
                return pd.to_datetime(val, errors='raise')
            except (ValueError, TypeError):
                return val
        return val

    df['transaction_date'] = df['transaction_date'].apply(safe_to_datetime).where(df['transaction_date'].notna(), None)
    df['disclosure_date'] = df['disclosure_date'].apply(safe_to_datetime).where(df['disclosure_date'].notna(), None)

    return df

# Main script (For Test)
if __name__ == "__main__":
    # Scrape and transform transactions data
    df_trades = scrape_and_transform_transactions()
    df_trades.to_csv('trades.csv', index=False)
    print("Trade data saved successfully.")