import requests
from bs4 import BeautifulSoup

def scrape_facebook_profiles(profile_urls):
    for profile_url in profile_urls:
        response = requests.get(profile_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Scraping profile information
            name_element = soup.find('title')
            name = name_element.text if name_element else "N/A"

            about_element = soup.find('div', {'class': '_5pbx userContent _3576'})
            about = about_element.text.strip() if about_element else "N/A"

            friends_element = soup.find('div', {'class': '_3d0 _3d1'})
            friends_count = friends_element.find('span').text if friends_element else "N/A"

            # Printing the scraped profile information
            print("Profile URL:", profile_url)
            print("Name:", name)
            print("About:", about)
            print("Friends:", friends_count)
            print()

        else:
            print(f"Failed to retrieve profile data for URL: {profile_url}")
            print()

# Example usage
profile_urls = [
    'https://www.facebook.com/zuck',
    'https://www.facebook.com/billgates',
    'https://www.facebook.com/elonmusk'
]  # Replace with the desired profile URLs

scrape_facebook_profiles(profile_urls)
