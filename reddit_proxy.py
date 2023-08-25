import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def scrape_user_data(username):
    # URL with the username as a placeholder
    url = f"https://www.reddit.com/user/{username}"
    # Proxies list
    proxies = [
        'http://proxy1.example.com:1234',
        'http://proxy2.example.com:5678',
        # Add more proxies here
    ]
    # Headers to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0'}

    max_retries = 3
    retry_delay = 1

    for retry in range(max_retries):
        try:
            # Select a random proxy from the list
            proxy = {'http': proxies[retry % len(proxies)]}
            # Returns a requests.models.Response object
            page = requests.get(url, headers=headers, proxies=proxy)
            page.raise_for_status()
            break  # Successful request, exit the loop
        except requests.exceptions.RequestException as e:
            print(f"Request failed. Retrying ({retry+1}/{max_retries})...")
            time.sleep(retry_delay)

    soup = BeautifulSoup(page.text, 'html.parser')

    # Find the element containing the username
    username_element = soup.find("h1", class_="_3LM4tRaExed4x1wBfK1pmg")

    if username_element is not None:
        username_text = username_element.text.strip()
        print(f"Full Name: {username_text}")
    else:
        print("Username not found on the profile page.")

    # Find the element containing the karma
    karma_element = soup.find("span", id="profile--id-card--highlight-tooltip--karma")

    if karma_element is not None:
        karma_text = karma_element.text.strip()
        print(f"Karma: {karma_text}")
    else:
        print("Karma not found on the profile page.")

    # Find the element containing the cake day
    cake_day_element = soup.find("span", id="profile--id-card--highlight-tooltip--cakeday")

    if cake_day_element is not None:
        cake_day_text = cake_day_element.text.strip()
        print(f"Cake Day: {cake_day_text}")
        # Calculate the age of the account
        current_year = datetime.now().year
        cake_day = datetime.strptime(cake_day_text, "%B %d, %Y")
        account_age = current_year - cake_day.year
        print(f"Age of Account: {account_age} years")
    else:
        print("Cake Day not found on the profile page.")

# # Usage with multiple usernames
# usernames = ["L_Industries", "example_user1", "example_user2"]

# for username in usernames:
#     scrape_user_data(username)
#     print("-----------------------")
#     time.sleep(1)  # Delay between requests to avoid overwhelming the server
