import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

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
    params = {
        'limit': limit
    }
    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        bills = data.get('bills', [])
        bill_list = []

        for bill in bills:
            bill_info = {
                'congress': bill.get('congress', 'N/A'),
                'bill_id': bill.get('number', 'N/A'),
                'title': bill.get('title', 'N/A'),
                'action_date': bill.get('latestAction', {}).get('actionDate', 'N/A'),
                'recent_update': bill.get('latestAction', {}).get('text', 'N/A'),
                'type': bill.get('type', 'N/A'),
                'chamber': bill.get('originChamber', 'N/A')
            }
            bill_list.append(bill_info)

        return pd.DataFrame(bill_list)

    else:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()

# Fetch news from the last 3 months
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

df_news = fetch_general_news_data('government', '2024-10-17', '2024-11-17')
print(df_news.head())
print('----------------------')
df_bills = pd.concat([fetch_recent_bills(117), fetch_recent_bills(118)], ignore_index=True)
print(df_bills.head())

df_bills.to_csv('bills.csv', index=False)
df_news.to_csv('government_news.csv', index=False)