import requests
from bs4 import BeautifulSoup
import concurrent.futures

# List of usernames
usernames = ["twinstar", "theposearchives", "Tomasz-Mro"]

# Function to scrape account information for a single username
def scrape_account_info(username):
    # URL of the website with the username
    url = f"https://www.deviantart.com/{username}"

    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        # Scrape the name
        name_element = soup.find("span", class_="_2UI2c")
        name = name_element.get_text(strip=True)
    except AttributeError:
        name = "Not found"

    try:
        # Scrape the more info
        more_info_element = soup.find("div", class_="_33syq")
        more_info = more_info_element.get_text(strip=True)
    except AttributeError:
        more_info = "Not found"

    try:
        # Scrape the number of watchers
        watchers_element = soup.find("span", class_="_1thFP")
        watchers = watchers_element.get_text(strip=True)
    except AttributeError:
        watchers = "Not found"

    try:
        # Scrape the number of deviations
        deviation_element = soup.find("span", class_="_1thFP")
        deviation = deviation_element.find("span").get_text(strip=True)
    except AttributeError:
        deviation = "Not found"

    try:
        # Scrape the pageviews
        pageviews_element = soup.find("div", class_="_1yr7V")
        pageviews = pageviews_element.get_text(strip=True)
    except AttributeError:
        pageviews = "Not found"

    # Return the scraped information
    return {
        "Username": username,
        "Name": name,
        "More info": more_info,
        "Watchers": watchers,
        "Deviation": deviation,
        "Pageviews": pageviews
    }

# Create a thread pool executor
executor = concurrent.futures.ThreadPoolExecutor()

# Submit the scraping tasks to the executor
futures = [executor.submit(scrape_account_info, username) for username in usernames]

# Wait for all tasks to complete and retrieve the results
results = [future.result() for future in concurrent.futures.as_completed(futures)]

# Print the scraped information
for result in results:
    for key, value in result.items():
        print(f"{key}: {value}")
    print("-----------------------------------")
