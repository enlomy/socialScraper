from playwright.sync_api import sync_playwright


def scrape_profile(url: str) -> dict:
    """
    Scrape a Twitter profile page for profile data.
    Return the profile data as a dictionary.
    """
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        page.goto(url)
        page.wait_for_selector("[data-testid='UserDescription']")

        # Extract profile data
        profile_data = {
            "name": page.inner_text("[data-testid='UserProfileHeader_Items'] > span"),
            "handle": page.inner_text("[data-testid='UserProfileHeader_Items'] > div"),
            "description": page.inner_text("[data-testid='UserDescription']"),
            "location": page.inner_text("[data-testid='UserProfileHeader_Items'] > span:nth-child(3)"),
            "website": page.inner_text("[data-testid='UserProfileHeader_Items'] > span:nth-child(4) a"),
            "join_date": page.inner_text("[data-testid='UserProfileHeader_Items'] > span:nth-child(6)"),
            "follower_count": page.inner_text("[data-testid='UserProfileHeader_Items'] > div:nth-child(3) span"),
            "following_count": page.inner_text("[data-testid='UserProfileHeader_Items'] > div:nth-child(4) span"),
            "tweet_count": page.inner_text("[data-testid='UserProfileHeader_Items'] > div:nth-child(5) span"),
        }

        browser.close()

        return profile_data


if __name__ == "__main__":
    profile_urls = [
        "https://twitter.com/Scrapfly_dev",
        "https://twitter.com/OpenAI",
        "https://twitter.com/Twitter",
    ]

    for url in profile_urls:
        try:
            profile_data = scrape_profile(url)
            print("Profile Data:")
            print(profile_data)
            print("-----")
        except Exception as e:
            print(f"An error occurred while scraping {url}: {str(e)}")
