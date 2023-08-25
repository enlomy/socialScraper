import asyncio
import aiohttp
from bs4 import BeautifulSoup
import nest_asyncio

nest_asyncio.apply()

async def scrape_user_profile(session, username):
    # Construct the URL for the user profile
    url = f"https://www.codecademy.com/profiles/{username}"

    async with session.get(url) as response:
        content = await response.text()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find and extract the desired information with error handling
    try:
        full_name = soup.find('p', {'data-testid': 'full-name-section'}).text
    except AttributeError:
        full_name = 'Full Name Not Found'

    try:
        username = soup.find('span', {'class': 'gamut-1bq9uel-Text e1xvzpfm2'}).text
    except AttributeError:
        username = 'Username Not Found'

    try:
        bio = soup.find('div', {'data-testid': 'bio-section'}).find('p').text
    except AttributeError:
        bio = 'Bio Not Found'

    try:
        location = soup.find('div', {'data-testid': 'role-section'}).find('p').text
    except AttributeError:
        location = 'Location Not Found'

    try:
        date_joined = soup.find('div', {'data-testid': 'date-section'}).find('p').text
    except AttributeError:
        date_joined = 'Date Joined Not Found'

    # Return the scraped information as a dictionary
    return {
        'Full Name': full_name,
        'Username': username,
        'Bio': bio,
        'Location': location,
        'Date Joined': date_joined
    }

async def main():
    # List of usernames to scrape
    usernames = ['twinstar', 'JohnDoe', 'JaneSmith']

    # Create an aiohttp session
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = asyncio.create_task(scrape_user_profile(session, username))
            tasks.append(task)

        # Wait for all tasks to complete
        profiles = await asyncio.gather(*tasks)

        # Print the scraped profiles
        for username, profile_data in zip(usernames, profiles):
            print(f"User Profile: {username}")
            for key, value in profile_data.items():
                print(f"{key}: {value}")
            print('---------------------------')

# Run the asyncio event loop
asyncio.run(main())
