import requests
from bs4 import BeautifulSoup
from typing import List
import re

class StockWatcher:
    def __init__(self, disclosure_date, transacation_date, ticker, sector, type, amount, representative, state, district, owner):
        self.disclosure_date = disclosure_date
        self.transaction_date = transacation_date
        self.ticker = ticker
        self.sector = sector
        self.type = type
        self.amount = amount
        self.representative = representative
        self.state = state
        self.district = district
        self.owner = owner

    def trade_scrape(url: str):
        trade_data = requests.get(url)
        if trade_data.status_code == 200:
            data = trade_data.json()
            trades = []
            for item in data:  # Adjust if JSON structure differs
                trade = StockWatcher(
                    disclosure_date = item.get("disclosure_date"),
                    transacation_date = item.get("transaction_date"),
                    ticker = item.get("ticker"),
                    sector = item.get("sector"),
                    type = item.get("type"),
                    amount = item.get("amount"),
                    representative=item.get("representative"),
                    state = item.get("state"),
                    district = item.get("district"),
                    owner = item.get("owner")
                )
                trades.append(trade)
            return trades
        return None

    def __str__(self):
        return (f"Date Disclosed: {self.disclosure_date}\n"
                f"Date of Transaction: {self.transaction_date}\n"
                f"Company: {self.ticker}\n"
                f"Sector of Company: {self.sector}\n"
                f"Type: {self.type}\n"
                f"Amount of Stock: {self.amount}\n"
                f"Representative: {self.representative}\n"
                f"State of Representative: {self.state}\n"
                f"District: {self.district}\n"
                f"Owner of Stock: {self.owner}\n")

url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
trades = StockWatcher.trade_scrape(url)

if trades:
    rep_name = input("Enter the representative's name: ")

    rep_trades = [trade for trade in trades if trade.representative.lower() == rep_name.lower()]

    if rep_trades:
        print(f"\nTrades involving {rep_name}:\n")
        for trade in rep_trades:
            print(trade)
    else:
        print(f"No trades found for representative {rep_name}.")
else:
    print("Failed to retrieve trade data.")
