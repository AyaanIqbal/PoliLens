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