import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

# Fetches recent bills that were passed in congress
def fetch_bills(congress_number, type, limit=250):
    API_KEY = os.getenv('CONGRESS_API_KEY')
    BASE_URL = f'https://api.congress.gov/v3/bill/{congress_number}/{type}'

    headers = {'X-API-Key': API_KEY}
    params = {
        'limit': limit,
        'offset': 0
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return pd.DataFrame()
    
    data = response.json()
    total_bills = data.get('pagination', {}).get('count', 0)
    print(f"Total bills to fetch: {total_bills}")

    bills = []
    total_pages = (total_bills // limit) + 1
    
    # Pagination loop
    for page in tqdm(range(total_pages), desc=f"Fetching bills for Congress {congress_number}"):
        params['offset'] = page * limit
        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            if response.status_code == 200:
                page_data = response.json()
                bills.extend(page_data.get('bills', []))
            else:
                print(f"Failed to fetch page {page}, status code: {response.status_code}")
        except Exception as e:
            print(f"Error on page {page}: {e}")

    # Process bills into structured data
    bill_list = []
    for bill in bills:
        unique_bill_id = f"{bill.get('congress', 'N/A')}-{bill.get('type', 'N/A')}{bill.get('number', 'N/A')}"

        bill_info = {
            'bill_id': unique_bill_id,
            'title': bill.get('title', 'N/A'),
            'congress': bill.get('congress', 'N/A'),
            'type': bill.get('type', 'N/A'),
            'chamber': bill.get('originChamber', 'N/A'),
            'action_date': bill.get('latestAction', {}).get('actionDate', 'N/A'),
            'recent_update': bill.get('latestAction', {}).get('text', 'N/A')
        }
        bill_list.append(bill_info)

    return pd.DataFrame(bill_list)

def fetch_congress_members(congress_number):
    BASE_URL = f'https://voteview.com/static/data/out/members/HS{congress_number}_members.json'

    response = requests.get(BASE_URL)

    # Data mapping
    party_codes = {
        100 : 'D', # Democrate
        200 : 'R', # Republican
        328 : 'I' # Independant
    }
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return pd.DataFrame()
    
    data = response.json()

    member_list = []
    for member in data:
        member_info = {
            'icpsr': member.get('icpsr', 'N/A'),
            'bioguide_id': member.get('bioguide_id', 'N/A'),
            'full_name': member.get('bioname', 'N/A'),
            'congress': member.get('congress', 'N/A'),
            'chamber': member.get('chamber', 'N/A'),
            'party': party_codes.get(member.get('party_code', 'N/A')),
            'state': member.get('state_abbrev', 'N/A')
        }
        member_list.append(member_info)

    return pd.DataFrame(member_list)

def fetch_member_votes():
    print('test')

# Fetches cosponsors for each bill and stores them in a separate DataFrame
def fetch_cosponsor_for_bill(df_bills, limit=250):
    API_KEY = os.getenv('CONGRESS_API_KEY')
    BASE_URL = 'https://api.congress.gov/v3/bill/'

    headers = {'X-API-Key': API_KEY}
    params = {'limit': limit}

    cosponsors_list = []

    for _, row in tqdm(df_bills.iterrows(), desc='Fetching cosponsors', total=len(df_bills)):
        bill_id = row['bill_id']
        congress = row['congress']
        bill_type = row['type']
        url = f"{BASE_URL}{congress}/{bill_type.lower()}/{bill_id}/cosponsors"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            cosponsors = data.get('cosponsors', [])
            for cosponsor in cosponsors:
                cosponsor_info = {
                    'bill_id': bill_id,
                    'bioguide_id': cosponsor.get('bioguideId', 'N/A'),
                    'first_name': cosponsor.get('firstName', 'N/A'),
                    'last_name': cosponsor.get('lastName', 'N/A'),
                    'party': cosponsor.get('party', 'N/A'),
                    'state': cosponsor.get('state', 'N/A'),
                    'date_sponsored': cosponsor.get('sponsorshipDate', 'N/A')
                }
                cosponsors_list.append(cosponsor_info)
        else:
            print(f"Error fetching cosponsors for {bill_id}: {response.status_code}")

    return pd.DataFrame(cosponsors_list)

# Main script (For Test)
if __name__ == "__main__":
    # Fetch news from the last 3 months
    # df_news = fetch_general_news_data('government', '2024-10-31', '2024-11-17')
    df_members = fetch_congress_members(116)
    df_members.to_csv('member.csv', index=False)

    # Fetch recent bills
    df_bills = pd.concat([fetch_bills(116, 'HR'), fetch_bills(116, 'S')], ignore_index=True)
    
    # Fetch cosponsors for each bill
    # df_cosponsors = fetch_cosponsor_for_each_bill(df_bills)

    # Save data to CSV files
    # df_news.to_csv('government_news.csv', index=False)
    df_bills.to_csv('bills.csv', index=False)
    # df_cosponsors.to_csv('cosponsors.csv', index=False)

    print("Data saved successfully.")