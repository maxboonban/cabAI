import requests
import json

# Define API URL
api_url = "https://cab.brown.edu/api/?page=fose&route=search"

# Corrected payload structure
payload = {
    "other": {"srcdb": "202420"},  # Correctly set 'srcdb' for the semester (Spring 2024)
    "criteria": [
        {"field": "keyword", "value": "csci"},  # Search term
        {"field": "is_ind_study", "value": "N"},  # Exclude independent study courses
        {"field": "is_canc", "value": "N"}  # Exclude canceled courses
    ]
}

# Headers to mimic browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Referer": "https://cab.brown.edu/",
    "X-Requested-With": "XMLHttpRequest"
}

# Send POST request
response = requests.post(api_url, json=payload, headers=headers)

# Check response
if response.status_code == 200:
    data = response.json()  # Convert response to JSON
    print(data['results'][0])  # Print raw JSON data
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

# # Define the filename
# filename = 'web_scrape/data_output.json'

# # Write the data to a JSON file
# with open(filename, 'w') as json_file:
#     json.dump(data, json_file, indent=4)

# print(f"Data has been written to {filename}")

