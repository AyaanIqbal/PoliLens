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
    
    def scrape_capitol_trades() -> List[poli_trade]:
        url = "https://www.capitoltrades.com/politicians"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        trades = []
        trade_row = soup.select('.trade-row')

        for row in trade_row:
            politician = row.select_one('.politician-name').text.strip()
            company = row.select_one('.company_name').text.strip()
            action = row.select_one('.trade-action').text.strip()
            amount = row.select_one('.trade-amount').text.strip()

            trade = poli_trade(politician, company, action, amount)
            trades.append(trade)
        return trades

    def main():
        capitol_trades = scrape_capitol_trades()
        for trade in capitol_trades:
            print(trade)

    if __name__ == "__main__":
        main()
