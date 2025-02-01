
import requests
import time

# Define API URLs
search_api_url = "https://cab.brown.edu/api/?page=fose&route=search"
details_api_url = "https://cab.brown.edu/api/?page=fose&route=details"

# Manually set `srcdb` for the correct semester (e.g., Spring 2025)
srcdb = "202420"  # Change if necessary

# Payload to search for CSCI courses
search_payload = {
    "other": {"srcdb": srcdb},
    "criteria": [
        {"field": "keyword", "value": ""},  # Search for Computer Science courses
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
    print(f"Found {len(courses)} courses.")

    # Step 2: Open text file to write structured course details
    with open("csci_courses.txt", "w", encoding="utf-8") as file:
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
            
            # Extract course description
            if details_response.status_code == 200:
                details_data = details_response.json()
                course_description = details_data.get("description", "No description available.")
            else:
                course_description = "Failed to fetch description."
            
            # Write structured course data to file
            file.write(f"Course Code: {course_code}\n")
            file.write(f"Title: {course.get('title', '')}\n")
            file.write(f"CRN: {crn}\n")
            file.write(f"Instructor: {course.get('instr', 'TBA')}\n")
            file.write(f"Meeting Time: {course.get('meets', 'TBA')}\n")
            file.write(f"Detailed Meeting Times: {course.get('meetingTimes', '[]')}\n")
            file.write(f"Start Date: {course.get('start_date', '')}\n")
            file.write(f"End Date: {course.get('end_date', '')}\n")
            file.write(f"Description: {course_description}\n")
            file.write("-" * 50 + "\n\n")  # Separator for readability

            time.sleep(1)  # Prevent server overload

    print("Course details saved to 'csci_courses.txt'.")

else:
    print(f"Failed to fetch course list. Status code: {search_response.status_code}")