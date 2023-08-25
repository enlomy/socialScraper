import requests
from bs4 import BeautifulSoup

def scrape_onlyfans_account(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the profile page. Please check the URL and try again.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    name_element = soup.select_one('h1.p-name')
    name = name_element.text.strip() if name_element else "N/A"
    images_element = soup.select_one('div.p-media-block[data-type="images"] span')
    images_count = images_element.text.strip() if images_element else "N/A"
    videos_element = soup.select_one('div.p-media-block[data-type="videos"] span')
    videos_count = videos_element.text.strip() if videos_element else "N/A"
    likes_element = soup.select_one('div.p-stats-block[data-type="likes"] span')
    likes_count = likes_element.text.strip() if likes_element else "N/A"
    followers_element = soup.select_one('div.p-stats-block[data-type="followers"] span')
    followers_count = followers_element.text.strip() if followers_element else "N/A"

    print("OnlyFans Account Details:")
    print("Name:", name)
    print("Images Posted:", images_count)
    print("Videos Posted:", videos_count)
    print("Likes:", likes_count)
    print("Followers:", followers_count)
    print("\n")

def scrape_pornhub_account(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the profile page. Please check the URL and try again.")
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    name_element = soup.select_one('div.usernameWrap')
    name = name_element.text.strip() if name_element else "N/A"
    location_element = soup.select_one('div.userDetails dd.location')
    location = location_element.text.strip() if location_element else "N/A"
    views_element = soup.select_one('div.userDetails dd.views')
    views_count = views_element.text.strip() if views_element else "N/A"
    career_element = soup.select_one('div.userDetails dd.careerStatus')
    career_status = career_element.text.strip() if career_element else "N/A"
    gender_element = soup.select_one('div.userDetails dd.gender')
    gender = gender_element.text.strip() if gender_element else "N/A"
    birth_element = soup.select_one('div.userDetails dd.birthplace')
    birth_place = birth_element.text.strip() if birth_element else "N/A"

    print("Pornhub Account Details:")
    print("Name:", name)
    print("City and Country:", location)
    print("Profile Views:", views_count)
    print("Career Status:", career_status)
    print("Gender:", gender)
    print("Birth Place:", birth_place)
    print("\n")

def main():
    onlyfans_url = "https://onlyfans.com/abbykbaee"
    pornhub_url = "https://www.pornhub.com/model/realtelarilove"

    scrape_onlyfans_account(onlyfans_url)
    scrape_pornhub_account(pornhub_url)

if __name__ == "__main__":
    main()