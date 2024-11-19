import requests
import json

def fetch_bioguide_id(url, search_name):
    # Fetch the JSON data from the URL
    response = requests.get(url)
    legislators = response.json()

    # Search for the legislator
    for legislator in legislators:
        full_name = f"{legislator['name']['first']} {legislator['name']['last']}"
        if search_name.lower() in full_name.lower():
            bioguide_id = legislator.get("id", {}).get("bioguide")
            return bioguide_id

    # If no matches are found, return None
    return None

# Main execution
if __name__ == "__main__":
    # URL to fetch the legislators JSON file
    json_url = "https://theunitedstates.io/congress-legislators/legislators-current.json"

    # Prompt for input
    name_to_search = input("Enter the name of the legislator: ").strip()

    # Call the function and handle the result
    bioguide_id = fetch_bioguide_id(json_url, name_to_search)
    if bioguide_id:
        print(bioguide_id)
    else:
        print(f"No Bioguide ID found for '{name_to_search}'.")
