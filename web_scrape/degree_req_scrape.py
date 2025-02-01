import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "https://bulletin.brown.edu/the-college/concentrations/comp/"

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
}

# Fetch the webpage
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the "Requirements for the Standard Track of the Sc.B. degree" section
    requirement_section = None

    for h3 in soup.find_all("h3"):  # Find all <h3> elements (subsection titles)
        if "Requirements for the Standard Track of the Sc.B. degree" in h3.text:
            requirement_section = h3.find_next("table")  # Find the table right after the heading
            break

    if requirement_section:
        with open("degree_requirements.txt", "w", encoding="utf-8") as file:
            file.write("Requirements for the Standard Track of the Sc.B. degree:\n\n")

            # Extract table rows
            rows = requirement_section.find_all("tr")
            for row in rows[1:]:  # Skip the header row
                columns = row.find_all("td")
                if len(columns) >= 2:
                    course_code = columns[0].text.strip()
                    course_name = columns[1].text.strip()
                    file.write(f"{course_code}: {course_name}\n")

        print("Degree requirements saved to 'degree_requirements.txt'.")

    else:
        print("Could not find the requirements section.")

else:
    print(f"Failed to fetch page. Status Code: {response.status_code}")