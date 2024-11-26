import pandas as pd
import requests

def scrape_and_transform_transactions():
    # URL of the JSON data
    url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"

    # Fetch the JSON data
    response = requests.get(url)
    response.raise_for_status() 

    # Load the data into a Pandas df
    data = response.json()
    df = pd.DataFrame(data)

    # Convert data categories  to datetime format
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    df['disclosure_date'] = pd.to_datetime(df['disclosure_date'], errors='coerce')

    # Convert 'disclosure_year' to an integer, handling invalid entries
    df['disclosure_year'] = pd.to_numeric(df['disclosure_year'], errors='coerce').fillna(0).astype(int)

    return df

# Example usage
transactions_df = scrape_and_transform_transactions()

print(transactions_df.head())
output_file = "house_stock_watcher.csv"

# save data as a csv file 
transactions_df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
print(transactions_df.head())
