import requests
from bs4 import BeautifulSoup
from typing import List

class StockWatcher:
    def __init__(self, disclosure_date, transaction_date, ticker, asset_desc, sector, type, amount, representative, state, district, owner):
        self.disclosure_date = disclosure_date
        self.transaction_date = transaction_date
        self.ticker = ticker
        self.asset_desc = asset_desc
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
            for item in data:
                trade = StockWatcher(
                    disclosure_date = item.get("disclosure_date"),
                    transaction_date = item.get("transaction_date"),
                    ticker = item.get("ticker"),
                    asset_desc = item.get("asset_description"),
                    sector = item.get("sector"),
                    type = item.get("type"),
                    amount = item.get("amount"),
                    representative = item.get("representative"),
                    state = item.get("state"),
                    district = item.get("district"),
                    owner = item.get("owner")
                )
                trades.append(trade)
            return trades
        return None

    def __str__(self):
        return (f"Disclosure Date: {self.disclosure_date}\n"
                f"Transaction Date: {self.transaction_date}\n"
                f"Ticker: {self.ticker}\n"
                f"Asset Description: {self.asset_desc}"
                f"Sector: {self.sector}\n"
                f"Type: {self.type}\n"
                f"Amount: {self.amount}\n"
                f"Representative: {self.representative}\n"
                f"State: {self.state}\n"
                f"District: {self.district}\n"
                f"Owner: {self.owner}\n")

url = "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.json"
trades = StockWatcher.trade_scrape(url)

if trades:
    categories = ["disclosure_date", "transaction_date", "ticker", "asset description", "sector", "type", 
                  "amount", "representative", "state", "district", "owner"]

    print("Available search categories:")
    for category in categories:
        print(f"- {category}")

    search_category = input("\nEnter the category you want to search in: ").strip().lower()

    if search_category in categories:
        search_term = input(f"Enter the value you want to search for in {search_category}: ").strip().lower()

        filtered_trades = [
            trade for trade in trades
            if getattr(trade, search_category, "").lower() == search_term
        ]

        if filtered_trades:
            print(f"\nTrades matching {search_category} = {search_term}:\n")
            for trade in filtered_trades:
                print(trade)
        else:
            print(f"No trades found for {search_category} = {search_term}.")
    else:
        print("Invalid search category. Please try again.")
else:
    print("Failed to retrieve trade data.")
