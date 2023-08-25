import time
import random
import threading
from queue import Queue
from nltk.corpus import words
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class YoutubeScraper:
    def __init__(self, base_search_url="https://www.youtube.com/results?search_query="):
        self.base_search_url = base_search_url
        self.chrome_options = Options()
        self.chrome_options.add_argument("--incognito")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("start-maximized")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 2,
            "profile.default_content_setting_values.notifications": 2
        })

        self.keywords = random.sample(words.words(), 2)
        self.channel_ids = set()
        self.channel_data = [] 
        self.unique_channel_count = 0
        self.url_queue = Queue()
        self.channel_ids_lock = threading.Lock()
        self.unique_channel_count_lock = threading.Lock()

    def process_url(self):
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)

        while not self.url_queue.empty():
            search_url = self.url_queue.get()
            driver.get(search_url)
            time.sleep(2)
            SCROLL_PAUSE_TIME = 2
            last_height = driver.execute_script("return document.documentElement.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)
                new_height = driver.execute_script("return document.documentElement.scrollHeight")

                if new_height == last_height or self.unique_channel_count >= 2:
                    break

                results = driver.find_elements(By.CSS_SELECTOR, 'a.yt-simple-endpoint.style-scope.yt-formatted-string')
                for result in results:
                    href = result.get_attribute('href')
                    with self.channel_ids_lock:
                        if href not in self.channel_ids:
                            self.channel_ids.add(href)
                            with self.unique_channel_count_lock:
                                self.unique_channel_count += 1

                last_height = new_height

        for channel_id in self.channel_ids:
            print("Channel Link:", channel_id)
            channel_data = {"Channel Link": channel_id}
            channel_url = channel_id + '/about'
            driver.get(channel_url)
            time.sleep(2)

            # Extract and print channel name
            channel_name_element = driver.find_element(By.CSS_SELECTOR, 'div.style-scope.ytd-channel-name yt-formatted-string.style-scope.ytd-channel-name')
            channel_name = channel_name_element.text
            print("Channel Name:", channel_name)
            channel_data["Channel Name"] = channel_name

            # Extract and print total videos
            total_videos_element = driver.find_element(By.CSS_SELECTOR, 'span.style-scope.yt-formatted-string')
            total_videos = total_videos_element.text
            print("Total Videos:", total_videos)
            channel_data["Total Videos"] = total_videos

            # Extract and print total subscribers
            total_subscribers_element = driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string#subscriber-count')
            total_subscribers = total_subscribers_element.text
            print("Total Subscribers:", total_subscribers)
            channel_data["Total Subscribers"] = total_subscribers

            # Extract and print Joining Date
            total_joining_date_elements = driver.find_elements(By.CSS_SELECTOR, 'div#right-column yt-formatted-string.style-scope.ytd-channel-about-metadata-renderer')

            if len(total_joining_date_elements) > 1:
                total_joining_date_elements = total_joining_date_elements[1].text  
                print("Joining Date:", total_joining_date_elements)
                channel_data["Joining Date"] = total_joining_date_elements
            else:
                print("Couldn't find the second 'yt-formatted-string' element!")

            # Extract and print total views
            total_views_elements = driver.find_elements(By.CSS_SELECTOR, 'div#right-column yt-formatted-string.style-scope.ytd-channel-about-metadata-renderer')

            if len(total_views_elements) > 1:
                total_views = total_views_elements[2].text 
                print("Total Views:", total_views)
                channel_data["Total Views"] = total_views
            else:
                print("Couldn't find the second 'yt-formatted-string' element!")

            print("--------------------------------------------------------")

            self.channel_data.append(channel_data)

        driver.quit()

    def start_scraping(self):
        for keyword in self.keywords:
            search_url = self.base_search_url + keyword
            self.url_queue.put(search_url)

        threads = [threading.Thread(target=self.process_url) for _ in range(5)]
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        df = pd.DataFrame(self.channel_data)

        df.to_excel('youtube_data.xlsx', index=False)


# usage
scraper = YoutubeScraper()
scraper.start_scraping()

