import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = '6834e2208e8f4986bda0d9ed757ae475'
BASE_URL = 'https://newsapi.org/v2/everything'

def fetch_general_news_data(query, from_date, to_date):
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

# Fetch news from the last 3 months
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

df_news = fetch_general_news_data('bill OR legislation OR congress OR government', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
df_news.to_csv('government_news.csv', index=False)