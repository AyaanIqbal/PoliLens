import requests
from bs4 import BeautifulSoup
from typing import List
import re

class poli_trade:
    def __init__(self, politician: str, company: str, action: str, amount: str):
        self.politician = politician
        self.company = company
        self.action = action
        self.amount - amount

    def __repr__(self):
        return f"poli_trade(politician='{self.politician}', company='{self.company}', action='{self.action}', amount='{self.amount}')"
    
    def scrape_trades() -> List[poli_trade]:
        url = "https://www.capitoltrades.com/politicians"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        trades = []
