import requests
from bs4 import BeautifulSoup

def scrape_capitol_trades(max_pages):
    # Base URL and initial setup
    base_url = "https://www.capitoltrades.com/trades?pageSize=96&page={}"
    trades = []
    
    # Iterate through the specified number of pages
    for current_page in range(1, max_pages + 1):
        print(f"Scraping page {current_page}...")
        url = base_url.format(current_page)
        response = requests.get(url)
        
        # Handle failed requests
        if response.status_code != 200:
            print(f"Failed to fetch page {current_page}. Status code: {response.status_code}")
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract trades from the current page
        trade_rows = soup.select("tbody > tr")  # Select all <tr> directly under <tbody>
        for row in trade_rows:
            trade_data = []
            cells = row.find_all("td")  # Locate all <td> cells in the row
            for cell in cells:
                trade_data.append(cell.text.strip())  # Extract and clean the text
            trades.append(trade_data)
    
    print(f"Scraped {len(trades)} trades from {max_pages} pages.")
    return trades

# User input for number of pages to scrape
max_pages = int(input("Enter the number of pages to scrape (each page contains 96 trades): "))
scraped_trades = scrape_capitol_trades(max_pages)

# Display scraped data
for trade in scraped_trades:
    print(trade)
