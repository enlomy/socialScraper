import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Define the list of user URLs to scrape
user_urls = [
    'https://t.me/twinstar',
    'https://t.me/jlaurey',
    # Add more user URLs here
]

# Define a function to scrape user information
async def scrape_user_info(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')
                name_element = soup.find('div', class_='tgme_page_title').find('span')
                username_element = soup.find('div', class_='tgme_page_extra')
                description_element = soup.find('div', class_='tgme_page_description')

                name = name_element.get_text(strip=True) if name_element else "N/A"
                username = username_element.get_text(strip=True) if username_element else "N/A"
                description = description_element.get_text(strip=True) if description_element else "N/A"

                # Print the extracted information
                print("Name:", name)
                print("Username:", username)
                print("Description:", description)
                print("----------------------")

            else:
                print(f"Failed to scrape user information from {url}. Status code: {response.status}")

# Create a list of coroutines for scraping user information concurrently
coroutines = [scrape_user_info(url) for url in user_urls]

# Run the coroutines concurrently
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*coroutines))
