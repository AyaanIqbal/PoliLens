import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

def scrape_capitol_trades_from_date(start_date):
    base_url = "https://www.capitoltrades.com/trades?pageSize=96&page={}"
    all_trades = []
    current_page = 1
    start_date = datetime.strptime(start_date, "%Y-%m-%d")

    while True:
        print(f"Scraping page {current_page}...")
        url = base_url.format(current_page)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        trade_rows = soup.select("tbody > tr")
        for row in trade_rows:
            cells = row.find_all("td")
            if len(cells) >= 8:
                # Handle "Published" column with today/yesterday cases
                published_text = cells[2].text.strip()
                if "today" in published_text.lower():
                    published_date = datetime.now()
                elif "yesterday" in published_text.lower():
                    published_date = datetime.now() - timedelta(days=1)
                else:
                    # Handle the '22 Nov2024' format
                    try:
                        published_date = datetime.strptime(published_text, "%d %b%Y")
                    except ValueError as e:
                        print(f"Error parsing date: {published_text}")
                        continue

                # Stop scraping if the date is earlier than the start date
                if published_date < start_date:
                    print("Reached trades before the start date.")
                    return pd.DataFrame(all_trades, columns=["Politician", "Company", "Published", "Traded", "Owner", "Type", "Size", "Price of Stock"])

                trade = {
                    "Politician": cells[0].text.strip(),
                    "Company": cells[1].text.strip(),
                    "Published": published_date.strftime("%Y-%m-%d"),
                    "Traded": cells[3].text.strip(),
                    "Owner": cells[5].text.strip(),
                    "Type": cells[6].text.strip(),
                    "Size": cells[7].text.strip(),
                    "Price of Stock": cells[8].text.strip(),
                }
                all_trades.append(trade)

        current_page += 1

    return pd.DataFrame(all_trades, columns=["Politician", "Company", "Published", "Traded", "Owner", "Type", "Size", "Price of Stock"])

# Set the start date and scrape trades
start_date = "2021-01-03"
trades_df = scrape_capitol_trades_from_date(start_date)

output_file = "capitol_trades_since_2021.csv"

# Save the data to a CSV file
trades_df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
print(trades_df.head())
