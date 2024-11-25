import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

def fetch_general_news_data(query, from_date, to_date):
    API_KEY = os.getenv('NEWS_API_KEY')
    BASE_URL = 'https://newsapi.org/v2/everything'

    params = {
        'q': query,
        'from': from_date,
        'to': to_date,
        'sortBy': 'relevancy',
        'apiKey': API_KEY,
        'language': 'en'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    articles = []
    for article in data['articles']:
        articles.append({
            'title': article['title'],
            'date': article['publishedAt'],
            'source': article['source']['name'],
            'url': article['url'],
            'content': article['content']
        })

    return pd.DataFrame(articles)

# Fetches recent bills that were passed in congress
def fetch_recent_bills(congress_number, limit=250):
    API_KEY = os.getenv('CONGRESS_API_KEY')
    BASE_URL = f'https://api.congress.gov/v3/bill/{congress_number}'

    headers = {'X-API-Key': API_KEY}
    params = {'limit': limit}
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        bills = data.get('bills', [])
        bill_list = []

        for bill in tqdm(bills, desc=f"Fetching bill details of congress {congress_number}"):
            bill_info = {
                'bill_id': bill.get('number', 'N/A'),
                'title': bill.get('title', 'N/A'),
                'congress': bill.get('congress', 'N/A'),
                'type': bill.get('type', 'N/A'),
                'chamber': bill.get('originChamber', 'N/A'),
                'action_date': bill.get('latestAction', {}).get('actionDate', 'N/A'),
                'recent_update': bill.get('latestAction', {}).get('text', 'N/A')
            }
            bill_list.append(bill_info)

        return pd.DataFrame(bill_list)

    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()
    
# Fetches cosponsors for each bill and stores them in a separate DataFrame
def fetch_cosponsor_for_each_bill(df_bills, limit=250):
    API_KEY = os.getenv('CONGRESS_API_KEY')
    BASE_URL = 'https://api.congress.gov/v3/bill/'

    headers = {'X-API-Key': API_KEY}
    params = {'limit': limit}

    cosponsors_list = []

    for _, row in tqdm(df_bills.iterrows(), desc='Fetching cosponsors', total=len(df_bills)):
        bill_id = row['bill_id']
        congress = row['congress']
        bill_type = row['type']
        url = f"{BASE_URL}{congress}/{bill_type.lower()}/{bill_id}/cosponsors"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            cosponsors = data.get('cosponsors', [])
            for cosponsor in cosponsors:
                cosponsor_info = {
                    'bill_id': bill_id,
                    'bioguide_id': cosponsor.get('bioguideId', 'N/A'),
                    'first_name': cosponsor.get('firstName', 'N/A'),
                    'last_name': cosponsor.get('lastName', 'N/A'),
                    'party': cosponsor.get('party', 'N/A'),
                    'state': cosponsor.get('state', 'N/A'),
                    'date_sponsored': cosponsor.get('sponsorshipDate', 'N/A')
                }
                cosponsors_list.append(cosponsor_info)
        else:
            print(f"Error fetching cosponsors for {bill_id}: {response.status_code}")

    return pd.DataFrame(cosponsors_list)

# Main script
if __name__ == "__main__":
    # Fetch news from the last 3 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    df_news = fetch_general_news_data('government', '2024-10-31', '2024-11-17')

    # Fetch recent bills from Congress 117 and 118
    df_bills = pd.concat([fetch_recent_bills(117), fetch_recent_bills(118)], ignore_index=True)

    # Fetch cosponsors for each bill
    df_cosponsors = fetch_cosponsor_for_each_bill(df_bills)

    # Save data to CSV files
    df_news.to_csv('government_news.csv', index=False)
    df_bills.to_csv('bills.csv', index=False)
    df_cosponsors.to_csv('cosponsors.csv', index=False)

    print("Data saved successfully.")