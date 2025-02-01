import requests
import time
import json

# Define API URLs
search_api_url = "https://cab.brown.edu/api/?page=fose&route=search"
details_api_url = "https://cab.brown.edu/api/?page=fose&route=details"

# Manually set `srcdb` based on Developer Tools (e.g., Spring 2024)
srcdb = "202420"  # Change if necessary

# Payload to search for all CSCI courses
search_payload = {
    "other": {"srcdb": srcdb},
    "criteria": [
        {"field": "keyword", "value": "csci"},  # Search for Computer Science courses
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

# Step 1: Fetch course list from `/search` API
search_response = requests.post(search_api_url, json=search_payload, headers=headers)

if search_response.status_code == 200:
    course_data = search_response.json()
    courses = course_data.get("results", [])  # Extract course list
    print(f"Found {len(courses)} CSCI courses.")

    # Step 2: Iterate over each course to fetch its description
    for course in courses:
        course_code = course["code"]  # e.g., "CSCI 0081"
        crn = course["crn"]  # e.g., "26980"
        
        # Payload for `/details` API
        details_payload = {
            "group": f"code:{course_code}",
            "key": f"crn:{crn}",
            "srcdb": srcdb,
            "matched": f"crn:{crn}",
            "userWithRolesStr": "!!!!!!"  # Required parameter
        }
        
        # Send request to `/details` API
        details_response = requests.post(details_api_url, json=details_payload, headers=headers)
        
        if details_response.status_code == 200:
            details_data = details_response.json()
            course_description = details_data.get("description", "No description available.")
            course["description"] = course_description  # Append description to original course data
        else:
            print(f"Failed to fetch description for {course_code} ({crn}).")
            course["description"] = "Failed to fetch description."

        time.sleep(1)  # Prevent server overload

    # Step 3: Save or return the final JSON
    final_data = {"srcdb": srcdb, "courses": courses}
    
    # Save to JSON file
    with open("csci_courses_with_descriptions.json", "w") as json_file:
        json.dump(final_data, json_file, indent=4)

    print("Final course data saved as 'csci_courses_with_descriptions.json'.")

else:
    print(f"Failed to fetch course list. Status code: {search_response.status_code}")