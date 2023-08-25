import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def scrape_user(session, username):
    # Make a GET request to the user's page
    url = f"https://replit.com/@{username}"
    async with session.get(url) as response:
        content = await response.text()

    # Parse the HTML content
    soup = BeautifulSoup(content, "html.parser")

    # Extract the Full Name
    full_name_element = soup.find("div", class_="css-fx43vb")
    full_name = full_name_element.find("h1", class_="css-1iqbb3j").text.strip() if full_name_element else "Not found"

    # Extract the Username
    username_element = soup.find("div", class_="css-1pwjctj")
    username = username_element.find("span", class_="css-162rtbe").text.strip() if username_element else "Not found"

    # Extract the number of Followers
    followers_element = soup.find("button", class_="css-1c2fc58")
    followers = followers_element.find("span", class_="css-10z1dta").text.strip() if followers_element else "Not found"

    # Extract the number of Following
    following_element = soup.find_all("button", class_="css-1c2fc58")
    if len(following_element) >= 2:
        following = following_element[1].find("span", class_="css-10z1dta").text.strip()
    else:
        following = "Not found"

    # Return the extracted information as a dictionary
    return {
        "Username": username,
        "Full Name": full_name,
        "Followers": followers,
        "Following": following
    }

async def main():
    # List of usernames to scrape
    usernames = ["twinstar", "exampleuser1", "exampleuser2"]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for username in usernames:
            task = asyncio.ensure_future(scrape_user(session, username))
            tasks.append(task)

        # Gather results from all tasks
        results = await asyncio.gather(*tasks)

        # Print the results
        for username, result in zip(usernames, results):
            print(f"Scraping user: {username}")
            for key, value in result.items():
                print(f"{key}: {value}")
            print('---------------------------')

# Run the main function
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
