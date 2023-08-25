import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
import nest_asyncio

# List of users to scrape
usernames = ['twinstar', 'Legsakimbo', 'fuckenkovacs', 'heethcliff', 'jlaurey']

# Function to scrape user information
async def scrape_user_info(session, username):
    try:
        # Send a GET request to the user page
        user_url = f'https://www.last.fm/user/{username}'
        async with session.get(user_url) as response:
            user_response = await response.text()
        user_soup = BeautifulSoup(user_response, 'html.parser')

        # Extract the title
        title_element = user_soup.find('h1', class_='header-title')
        title = title_element.find('a').text.strip()

        # Extract the scrobble since
        scrobble_since_element = user_soup.find('span', class_='header-scrobble-since')
        scrobble_since = scrobble_since_element.text.strip().split('since ')[1]

        # Extract the display name
        display_name_element = user_soup.find('span', class_='header-title-display-name')
        display_name = display_name_element.text.strip()

        # Extract the scrobbles
        scrobbles_element = user_soup.find('div', class_='header-metadata-display')
        scrobbles = scrobbles_element.find('a').text.strip()

        return title, scrobble_since, display_name, scrobbles
    except AttributeError:
        print(f'Error: Some elements not found for user "{username}"')
    except aiohttp.ClientError:
        print(f'Error: Request failed for user "{username}"')

# Function to scrape follower count
async def scrape_followers_count(session, username):
    try:
        # Send a GET request to the followers page
        followers_url = f'https://www.last.fm/user/{username}/followers'
        async with session.get(followers_url) as response:
            followers_response = await response.text()
        followers_soup = BeautifulSoup(followers_response, 'html.parser')

        # Extract the followers count
        followers_count_element = followers_soup.find('h1', class_='content-top-header')
        
        if followers_count_element:
            followers_count_text = followers_count_element.text.strip()
            followers_count_match = re.findall(r'\d+', followers_count_text)

            if followers_count_match:
                followers_count = followers_count_match[0]
                return followers_count
            else:
                print(f'Error: Followers count not found for user "{username}"')
        else:
            print(f'Error: Followers count element not found for user "{username}"')
    
    except aiohttp.ClientError:
        print(f'Error: Request failed for user "{username}"')

# Function to scrape following count
async def scrape_following_count(session, username):
    try:
        # Send a GET request to the following page
        following_url = f'https://www.last.fm/user/{username}/following'
        async with session.get(following_url) as response:
            following_response = await response.text()
        following_soup = BeautifulSoup(following_response, 'html.parser')

        # Extract the following count
        following_count_element = following_soup.find('h1', class_='content-top-header')
        
        if following_count_element:
            following_count_text = following_count_element.text.strip()
            following_count_match = re.findall(r'\d+', following_count_text)

            if following_count_match:
                following_count = following_count_match[0]
                return following_count
            else:
                print(f'Error: Following count not found for user "{username}"')
        else:
            print(f'Error: Following count element not found for user "{username}"')

    except aiohttp.ClientError:
        print(f'Error: Request failed for user "{username}"')

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            tasks.append(scrape_user_info(session, username))
            tasks.append(scrape_followers_count(session, username))
            tasks.append(scrape_following_count(session, username))

        results = await asyncio.gather(*tasks)

        for i in range(0, len(results), 3):
            username = usernames[i // 3]
            title, scrobble_since, display_name, scrobbles = results[i]
            followers_count = results[i + 1]
            following_count = results[i + 2]

            # Print the extracted information
            print(f'Processing user "{username}"...')
            print('Title:', title)
            print('Scrobble Since:', scrobble_since)
            print('Display Name:', display_name)
            print('Scrobbles:', scrobbles)
            print('Followers:', followers_count)
            print('Following:', following_count)
            print('-----------------------------------')

# Run the event loop using nest_asyncio
nest_asyncio.apply()
asyncio.run(main())
