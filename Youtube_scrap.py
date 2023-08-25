import requests

def scrape_user_profile(api_key, username):
    url = f"https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,contentDetails,statistics",
        "forUsername": username,
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "items" in data:
        item = data["items"][0]
        # Extract the desired information from the response
        profile_data = {
            "username": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "subscriber_count": item["statistics"]["subscriberCount"],
            "view_count": item["statistics"]["viewCount"],
            "video_count": item["statistics"]["videoCount"]
        }
        return profile_data

    return None

# API key obtained from the Google Developer Console
api_key = "AIzaSyA5mLlnwmzjTZujIB1l4bOsoU9Rp1Yz4so"

# List of usernames to scrape
usernames = ["pewdiepie", "tseries", "checkgate", "setindia", "WWEFanNation", "corycotton", "zeemusiccompany", "EdSheeran", "NewOnNetflix", "BuzzFeedVideo", "NatGeoWild"]  # Add more usernames as needed

for username in usernames:
    profile_data = scrape_user_profile(api_key, username)
    if profile_data:
        # Process the profile data as needed
        print(profile_data)
    else:
        print(f"Profile data not found for username: {username}")
