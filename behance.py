import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_data(session, user):
    url = f'https://www.behance.net/{user}'
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                name = soup.find('h1', class_='ProfileCard-userFullName-ule').text.strip()
                role = soup.find('p', class_='ProfileCard-line-fVO e2e-Profile-occupation').text.strip()
                company = soup.find('p', class_='ProfileCard-line-fVO e2e-Profile-company').text.strip()
                location = soup.find('span', class_='e2e-Profile-location').text.strip()
                followers = soup.find('a', class_='UserInfo-statValue-d3q e2e-UserInfo-statValue-followers-count').text.strip()
                following = soup.find('a', href=f'/{user}/following?background=/profile/{user}').text.strip()
                appreciations = soup.find('td', class_='UserInfo-statColumn-NsR UserInfo-statValue-d3q').find('a').text.strip()
                project_views = soup.find_all('td', class_='UserInfo-statColumn-NsR UserInfo-statValue-d3q')[1].find('a').text.strip()
                profile_image_url = soup.find('img', class_='AvatarImage-avatarImage-PUL')['src']

                print('Name:', name)
                print('Role:', role)
                print('Company:', company)
                print('Location:', location)
                print('Followers:', followers)
                print('Following:', following)
                print('Appreciations:', appreciations)
                print('Project Views:', project_views)
                print('Profile Image URL:', profile_image_url)
                print('---------------------------------------------')
            else:
                print(f'Error: Failed to retrieve data for user {user}')
    except Exception as e:
        print(f'Error: An exception occurred while scraping data for user {user}: {str(e)}')


async def main(users):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user in users:
            tasks.append(scrape_user_data(session, user))
        await asyncio.gather(*tasks)


users = ['twinstar', 'another_user', 'example_user']

loop = asyncio.get_event_loop()
loop.run_until_complete(main(users))
