import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

def scrape_github_profile(username):
    url = f"https://www.github.com/{username}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    username_element = soup.find("span", class_="p-nickname vcard-username d-block")
    username = username_element.get_text(strip=True) if username_element else None

    fullname_element = soup.find("span", class_="p-name vcard-fullname d-block overflow-hidden")
    fullname = fullname_element.get_text(strip=True) if fullname_element else None

    location_element = soup.find("li", class_="vcard-detail pt-1 hide-sm hide-md", itemprop="homeLocation")
    location = location_element.find("span", class_="p-label").get_text(strip=True) if location_element else None

    organization_element = soup.find("li", class_="vcard-detail pt-1 hide-sm hide-md", itemprop="worksFor")
    organization = organization_element.find("span", class_="p-org").get_text(strip=True) if organization_element else None

    social_links = soup.find_all("li", itemprop="social")
    social_links_list = [link.find("a", class_="Link--primary").get("href") for link in social_links] if social_links else None

    timezone_element = soup.find("li", class_="vcard-detail pt-1 hide-sm hide-md", itemprop="localTime")
    timezone = timezone_element.find("span", class_="p-label").get_text(strip=True) if timezone_element else None

    followers_element = soup.find("span", class_="text-bold color-fg-default")
    followers = followers_element.get_text(strip=True) if followers_element else None

    following_element = soup.find("a", class_="Link--secondary no-underline no-wrap")
    following = following_element.find("span").get_text(strip=True) if following_element else None

    return {
        "Username": username,
        "Full Name": fullname,
        "Location": location,
        "Organization": organization,
        "Social Links": social_links_list,
        "Time Zone": timezone,
        "Followers": followers,
        "Following": following
    }

def scrape_profiles(usernames):
    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_github_profile, usernames)

    for username, result in zip(usernames, results):
        print("Scraping profile for", username)
        for key, value in result.items():
            print(key + ":", value)
        print('----------------------------------------')

# List of usernames to scrape
usernames = [
    "twinstar",
    "JLaurey",
    "octocat",
    "defunkt",
    "mojombo",
    "pengwynn",
    "pjhyett",
    "schacon",
    "kevinclark",
    "technoweenie",
    "atmos",
    "jekyll",
    "benbalter",
    "holman",
    "dhh",
    "mojombo",
    "tpope",
    "sindresorhus",
    "addyosmani",
    "taylorotwell"
]

# Scrape profiles for each username
scrape_profiles(usernames)
