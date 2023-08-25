import asyncio
import aiohttp
from bs4 import BeautifulSoup

# List of users to scrape
users = ["willdowd", "example1", "example2", ...]

async def scrape_user(session, user):
    url = f"https://substack.com/@{user}"

    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()

                soup = BeautifulSoup(content, "html.parser")

                # Extract the name
                name_element = soup.find("h1", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-32--oRWIM frontend-pencraft-Text-module__weight-bold--Ps9DB frontend-pencraft-Text-module__font-display--KlbfE frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__header1--fN7A4")
                name = name_element.text.strip()

                # Extract the username
                username_element = soup.find("a", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-11--k1e8b frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-medium--x7khA frontend-pencraft-Text-module__font-meta--U_nxy frontend-pencraft-Text-module__color-secondary--WRADg frontend-pencraft-Text-module__transform-uppercase--IDkUL frontend-pencraft-Text-module__decoration-hover-underline--BEYAn frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__meta--jzHdd")
                username = username_element.text.strip()

                # Extract the bio
                bio_element = soup.find("div", class_="pencraft frontend-pencraft-Box-module__reset--VfQY8 frontend-pencraft-Text-module__size-14--Ume6q frontend-pencraft-Text-module__line-height-20--p0dP8 frontend-pencraft-Text-module__weight-normal--s54Wf frontend-pencraft-Text-module__font-text--QmNJR frontend-pencraft-Text-module__color-primary--ud4Z0 frontend-pencraft-Text-module__reset--dW0zZ frontend-pencraft-Text-module__body4--Pl3xY")
                bio = bio_element.text.strip()

                # Store the scraped data in the desired persistent storage (e.g., database, file system)

                print("Name:", name)
                print("Username:", username)
                print("Bio:", bio)

                print("------------------------------------")  # Separator

            else:
                print(f"Error scraping user {user}. Status code: {response.status}")

    except Exception as e:
        print(f"Error scraping user {user}: {str(e)}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user in users:
            task = asyncio.create_task(scrape_user(session, user))
            tasks.append(task)

        await asyncio.gather(*tasks)

# Run the scraping process
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
