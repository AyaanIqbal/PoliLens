import requests
from bs4 import BeautifulSoup

url = "https://www.quiverquant.com/congresstrading/"

response = requests.get(url)
response.raise_for_status() 


soup = BeautifulSoup(response.content, "html.parser")

trades_section = soup.find("div", {"class": "table-outer"}) 
if not trades_section:
    raise Exception("Could not find the trades section on the page")

rows = trades_section.find_all("tr")
trades = []

trades_amount = input("How many trades would you like to see: ")

for row in rows[1:int(trades_amount)+1]:
    cells = row.find_all("td")
    if len(cells) < 6:  # Ensure all required columns exist
        continue
    
    trade = {
        "stock": cells[0].get_text(strip=True),
        "transaction": cells[1].get_text(strip=True),  # Amount and type
        "politician": cells[2].get_text(strip=True),
        "filed": cells[3].get_text(strip=True),
        "traded": cells[4].get_text(strip=True),
        "description": cells[5].get_text(strip=True),
        "estimated_return": cells[6].get_text(strip=True)
    }
    trades.append(list(trade.values()))

# Print or process the resulting trades array
for trade in trades:
    print(trade)
