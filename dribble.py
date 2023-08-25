import concurrent.futures
import requests
from bs4 import BeautifulSoup

def scrape_profile(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if there's an HTTP error

        soup = BeautifulSoup(response.content, "html.parser")

        name_element = soup.find("h1", class_="masthead-profile-name")
        name = name_element.text.strip()

        location_element = soup.find("p", class_="masthead-profile-locality")
        location = location_element.text.strip()

        bio_element = soup.find("div", class_="bio")
        bio = bio_element.p.text.strip()

        image_element = soup.find("img", class_="profile-avatar")
        image_url = image_element["src"]

        member_since_element = soup.find("p", class_="info-item created")
        member_since = member_since_element.span.text.strip()

        social_links_list = []
        social_links_elements = soup.find_all("a", class_="js-event-social")
        for link_element in social_links_elements:
            social_link = link_element["data-destination"]
            social_links_list.append(social_link)

        return {
            'url': url,
            'name': name,
            'location': location,
            'bio': bio,
            'image_url': image_url,
            'member_since': member_since,
            'social_links': social_links_list
        }
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while scraping {url}: {e}")
    except Exception as e:
        print(f"Error occurred while processing {url}: {e}")

    return None

# List of user account URLs to scrape
user_urls = [
    "https://dribbble.com/zoeyshen/about",
    "https://dribbble.com/Twinstar/about",
    "https://dribbble.com/VIDOR/about",
    "https://dribbble.com/arshakir/about",
    "https://dribbble.com/rosen/about",
    "https://dribbble.com/vikestan/about",
    # Add more user URLs here...
]

scraped_profiles = []

# Set the maximum number of threads to control concurrency
max_threads = 10

with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Submit scraping tasks
    futures = [executor.submit(scrape_profile, url) for url in user_urls]

    # Retrieve the results as they complete
    for future in concurrent.futures.as_completed(futures):
        try:
            profile = future.result()
            if profile:
                scraped_profiles.append(profile)
        except Exception as e:
            print("Error occurred:", e)

# Print the scraped profiles
for profile in scraped_profiles:
    print("URL:", profile['url'])
    print("Name:", profile['name'])
    print("Location:", profile['location'])
    print("Bio:", profile['bio'])
    print("Profile Image URL:", profile['image_url'])
    print("Member Since:", profile['member_since'])
    print("Social Links:", profile['social_links'])
    print('-------------------------------------------------')
