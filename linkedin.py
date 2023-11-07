from zenrows import ZenRowsClient 
import time
import asyncio 
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs 
 
zenrows_params = {"js_render":"true","antibot":"true","premium_proxy":"true"}
# Set concurrency and retries
client = ZenRowsClient("7b26afa746c5aa85d837d1440875a2c44279615a",concurrency=10, retries=1) 
 

# Create a function to parse HTML using Beautiful Soup
def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Manipulate the Beautiful Soup object to extract data as needed
    return soup

async def scrap_linkedin(urls): 
    responses = await asyncio.gather(*[client.get_async(url,zenrows_params) for url in urls]) 

    result = []
    for idx,response in enumerate(responses): 
        original_url = parse_qs(urlparse(response.request.url).query)["url"]
        
        if response.status_code == 200:
            # print({ 
            #     "response": response, 
            #     "status_code": response.status_code, 
            #     "request_url": original_url, 
            # }) 
            soup = parse_html(response.content)
            name_element = soup.find('h1', class_='top-card-layout__title')
            role_element = soup.find('h2', class_='top-card-layout__headline')
            info_div = soup.find('h3', class_='top-card-layout__first-subline')
            # Find the first span child
            location_element = info_div.find_all('span')
            # name_element = h1_element.find('span')
            elems = soup.find_all('span', class_='top-card-link__description')
            # Select the second element (Python indexing starts from 0, hence the 2nd element will be at index 1)
            experience_element = elems[0]
            education_element = elems[1] if len(elems) > 1 else None

            # Get Avatar Url
            avatar_url=""
            div_element = soup.find('div', class_='profile_header--profileHeaderAvatarContainer--7f99T')
            if div_element:
                # Get the style attribute value
                avatar_img = div_element.find('img')

                # Extract the image URL from the style attribute
                avatar_url = avatar_img['src'] if avatar_img else ""
            else:
                avatar_url=""

            # span_follow = soup.find_all('span', class_='profile_resources_grid--followsDataCount--HPMnb')


            name = name_element.get_text(strip=True) if name_element else ""
            role = role_element.get_text(strip=True) if role_element else ""
            location = location_element[0].get_text(strip=True) if location_element[0] else ""
            experience = experience_element.get_text(strip=True) if experience_element else ""
            education = education_element.get_text(strip=True) if education_element else ""
            # follower = span_follow[0].get_text(strip=True) if span_follow[0] else ""
            # following = span_follow[1].get_text(strip=True) if span_follow[1] else ""

            print({
                "Name": name,
                "Role": role,
                "location": location,
                "experience": experience,
                "education": education,
                # "Follower": follower,
                # "Following": following,
                # "Avatar-link": avatar_url,
                # "Link": urls[idx]
            })
        else:
            print(f"Not available --> {urls[idx]}")
            # print(response.content) 
 
if __name__ == '__main__':
    st_time = time.monotonic()
    urls = [
        "https://www.linkedin.com/in/michael-bage-10214a112",
        # "https://www.linkedin.com/in/michael-bage-242a6b204",
        # "https://www.linkedin.com/in/michael-bage-4781a970",
        # "https://www.linkedin.com/in/mike-bage-78757532",
        # "https://uk.linkedin.com/in/michael-bage-13125447",
        # "https://uk.linkedin.com/in/michael-bage-cgli-tmiet-33b87643",
        # "https://uk.linkedin.com/in/michael-bage-8397154b",
        # "https://uk.linkedin.com/in/mike-bage-357bb1b9",
        # "https://br.linkedin.com/in/michael-bag%C3%A9-576968122"
    ]

    asyncio.run(scrap_linkedin(urls))

    print("\033[32m"+f"Extracting Done ... [{time.monotonic() - st_time:.2f}s]." + "\033[0m")