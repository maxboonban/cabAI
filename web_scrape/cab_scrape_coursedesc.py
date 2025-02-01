import requests

# Define API URLs
details_api_url = "https://cab.brown.edu/api/?page=fose&route=details"

# Manually set `srcdb` based on what works in Developer Tools
srcdb = "202420"  # Change this if necessary

# Course details for CSCI 0081
course_code = "CSCI 0081"
crn = "26980"

# Payload to fetch course details
details_payload = {
    "group": f"code:{course_code}",
    "key": f"crn:{crn}",
    "srcdb": srcdb,  # Semester database
    "matched": f"crn:{crn}",
    "userWithRolesStr": "!!!!!!"  # Required field
}

# Headers to mimic browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json",
    "Referer": "https://cab.brown.edu/",
    "X-Requested-With": "XMLHttpRequest"
}

# Send POST request to fetch course details
response = requests.post(details_api_url, json=details_payload, headers=headers)

# Check response
if response.status_code == 200:
    details_data = response.json()
    course_description = details_data.get("description", "No description available.")
    # print(f"CSCI 0081 (CRN: {crn}) - Description:\n{course_description}")
    print(details_data['description'])
else:
    print(f"Failed to fetch details for CSCI 0081. Status code: {response.status_code}")