import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def scrape_user_data(username):
    # URL with the username as a placeholder
    url = f"https://www.reddit.com/user/{username}"
    # Proxies list
    proxies = [
        'http://7b26afa746c5aa85d837d1440875a2c44279615a:@proxy.zenrows.com:8001',
    ]
    # Headers to mimic a browser visit
    headers = {'User-Agent': 'Mozilla/5.0'}

    max_retries = 3
    retry_delay = 0.001  # set to 1 millisecond

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

    # Find the element containing the full name
    full_name_element = soup.find("h1", class_="_3LM4tRaExed4x1wBfK1pmg")

    if full_name_element is not None:
        full_name_text = full_name_element.text.strip()
        print(f"Full Name: {full_name_text}")
    else:
        print("Full Name not found on the profile page.")

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
    
    # Find the element containing the profile avatar URL
    profile_avatar_element = soup.find("div", class_="_34XIqvI8-YT1wukR_W8vj6")
    
    if profile_avatar_element is not None:
        profile_avatar_image = profile_avatar_element.find("img", class_="_2bLCGrtCCJIMNCZgmAMZFM")
        
        if profile_avatar_image is not None:
            profile_avatar_url = profile_avatar_image.get("src")
            print(f"Profile avatar URL: {profile_avatar_url}")
        else:
            print("Profile avatar image not found on the profile page.")
    else:
        print("Profile avatar element not found on the profile page.")

# Usage with multiple usernames
usernames = ["L_Industries", "_kasp", "MoonSerenade", "CrimsonWanderer","andersson","twinstar","SilverLioness","ElectricJester","MidnightWhisper","SapphireStorm","EnigmaticScribe","NebulaDreamer","EmberShadow","RadiantPhoenix","an_k","and_k","ande_k","an_ka","a_kas","an_kas","k_a","k_ande","k_ander","k_anders","ka_and","kas_an","kasp_a"]

for username in usernames:
    scrape_user_data(username)
    print("-----------------------")
    time.sleep(0.001)  # set to delay by 1 millisecond
