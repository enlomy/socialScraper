import instaloader
import os
import re
import concurrent.futures

proxies = [
    'http://7b26afa746c5aa85d837d1440875a2c44279615a:@proxy.zenrows.com:8001',
    'http://proxy2:port2',
    'http://proxy3:port3',
    # Add more proxy URLs as needed
]

def scrape_profile(username):
    try:
        # Creating an instance of the Instaloader class
        bot = instaloader.Instaloader()

        # Load session from a file if available
        if os.path.isfile("session"):
            bot.load_session_from_file("session")
        else:
            # Authenticate if session file doesn't exist
            bot.login("<your_username>", "<your_password>")
            # Save session to a file for future use
            bot.save_session_to_file("session")

        # Set the proxy URL in environment variables
        proxy = proxies[hash(username) % len(proxies)]
        os.environ['http_proxy'] = proxy

        # Loading a profile from an Instagram handle
        profile = instaloader.Profile.from_username(bot.context, username)

        print("Username: ", profile.username)
        print("User ID: ", profile.userid)
        print("Number of Posts: ", profile.mediacount)
        print("Followers Count: ", profile.followers)
        print("Following Count: ", profile.followees)
        print("Bio: ", profile.biography)
        print("External URL: ", profile.external_url)

        emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", profile.biography)
        print("Emails extracted from the bio:")
        print(emails)
        print("---------------------------------------")

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile with username '{username}' does not exist.")
    except instaloader.exceptions.ConnectionException:
        print(f"An error occurred while accessing profile '{username}'. Please check your internet connection.")
    except Exception as e:
        print(f"An error occurred while processing profile '{username}': {str(e)}")

def extract_emails_from_profiles(usernames):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(scrape_profile, usernames)

# Example usage
usernames = ['michaelbagebage', 'leomessi', 'cristiano', 'jenniferaniston', 'selenagomez', 'kevinhart4real', 'nasa', 'natgeo', 'therock', 'kyliejenner', 'barackobama', 'kimkardashian', 'neymarjr', 'katyperry', 'arianagrande', 'elonmusk', 'dwaynejohnson', 'taylorswift', 'realmadrid', 'nike', 'instagram']
extract_emails_from_profiles(usernames)
