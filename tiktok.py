import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://www.tiktok.com/@{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')
            username_element = soup.find('h1', class_='tiktok-fqd5k2-H1ShareTitle')
            name_element = soup.find('h2', class_='tiktok-1d3qdok-H2ShareSubTitle')
            following_count_element = soup.find('strong', {'data-e2e': 'following-count'})
            follower_count_element = soup.find('strong', {'data-e2e': 'followers-count'})
            user_bio_element = soup.find('h2', class_='tiktok-vdfu13-H2ShareDesc')
            link_element = soup.find('span', class_='tiktok-847r2g-SpanLink')
            
            username = username_element.get_text(strip=True) if username_element else ""
            name = name_element.get_text(strip=True) if name_element else ""
            following_count = following_count_element.get_text(strip=True) if following_count_element else ""
            follower_count = follower_count_element.get_text(strip=True) if follower_count_element else ""
            user_bio = user_bio_element.get_text(strip=True) if user_bio_element else ""
            link = link_element.get_text(strip=True) if link_element else ""
            
            return {
                "Username": username,
                "Name": name,
                "Following Count": following_count + " following",
                "Follower Count": follower_count + " followers",
                "User-bio": user_bio,
                "Link": link
            }
        else:
            print(f"Error retrieving data for user: {username}")
            return None

async def scrape_users(usernames):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = asyncio.ensure_future(scrape_user_info(session, username))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results


if __name__ == '__main__':
    usernames = ["bareandneutral", "sirbalocomedy_", "melekazad", "gracino___", "anthonumeh"]

    try:
        loop = asyncio.get_event_loop()
        scraped_data = loop.run_until_complete(scrape_users(usernames))
        for data in scraped_data:
            if data:
                for key, value in data.items():
                    print(f"{key}: {value}")
                print("---------------------------")
    except RuntimeError as e:
        if str(e) == "Event loop is closed":
            pass
        else:
            raise  # Re-raise other RuntimeError exceptions
    finally:
        loop.close()