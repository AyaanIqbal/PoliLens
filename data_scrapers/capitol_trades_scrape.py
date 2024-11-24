import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_capitol_trades_to_dataframe(trade_limit):
    base_url = "https://www.capitoltrades.com/trades?pageSize=96&page={}"
    all_trades = []
    current_page = 1

    while len(all_trades) < trade_limit:
        print(f"Scraping page {current_page}...")
        url = base_url.format(current_page)
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Go through each trade on every page
        trade_rows = soup.select("tbody > tr")
        for row in trade_rows:
            cells = row.find_all("td")  
            if len(cells) >= 8:  
                trade = {
                    "Politician": cells[0].text.strip(),
                    "Company": cells[1].text.strip(),
                    "Published": cells[2].text.strip(),
                    "Traded": cells[3].text.strip(),
                    "Owner": cells[5].text.strip(),
                    "Type": cells[6].text.strip(),
                    "Size": cells[7].text.strip(),
                    "Price of Stock": cells[8].text.strip(),
                }
                all_trades.append(trade)
                if len(all_trades) >= trade_limit: # continue until trade amount input is rached
                    break
        
        current_page += 1

    trades_df = pd.DataFrame(all_trades, columns=["Politician", "Company", "Published", "Traded", "Owner", "Type", "Size", "Price of Stock"])
    
    print(f"Scraped {len(all_trades)} trades.")
    return trades_df

trade_limit = int(input("Enter the number of trades to scrape: "))
# take scraped data as dataframe
trades_df = scrape_capitol_trades_to_dataframe(trade_limit)

output_file = "capitol_trades.csv"

# save data as a csv file 
trades_df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
print(trades_df.head())
