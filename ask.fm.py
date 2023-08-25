import asyncio
import aiohttp
import re
from bs4 import BeautifulSoup


async def scrape_user_info(session, username):
    url = f"https://ask.fm/{username}"
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')

            # Get Avatar Url
            avatar_url=""
            a_element = soup.find('a', class_='userAvatar-big')
            if a_element:
                # Get the style attribute value
                style_attr = a_element.get('style')

                # Extract the image URL from the style attribute
                start_index = style_attr.find('url(') + 4
                end_index = style_attr.find(')')

                avatar_url = style_attr[start_index:end_index]
            else:
                avatar_url=""
            # Get Name Element
            name_element = soup.find('span', class_='ellipsis lh-spacy')
            location_element = soup.find('div', class_='mv-2 mh-2 md:mh-0 pl-6 position-relative text-gray-200 icon-location')
            bio_element = soup.find('div', class_='mv-2 mh-2 md:mh-0 pl-6 position-relative text-gray-200 icon-bio')
            posts_elemtnt = soup.find('div', class_='profileTabAnswerCount text-large')
            likes_elemtnt = soup.find('div', class_='profileTabLikeCount text-large')



            full_name = name_element.get_text(strip=True) if name_element else ""
            location = location_element.get_text(strip=True) if location_element else ""
            bio = bio_element.get_text(strip=True) if bio_element else ""
            posts = posts_elemtnt.get_text(strip=True) if posts_elemtnt else ""
            likes = likes_elemtnt.get_text(strip=True) if likes_elemtnt else ""
            # Find the specific 'div' element with the given class
            return {
                "Username": username,
                "Name": full_name,
                "Posts": posts + " posts",
                "Likes": likes + " likes",
                "User-bio": bio,
                "Avatar-link": avatar_url,
                "Location": location,
                "Link": url
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
    usernames = ["mmadeehaa","akira","michael"]
    # usernames = ["bareandneutral", "sirbalocomedy_", "melekazad", "gracino___", "anthonumeh"]

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