import instaloader
import pandas as pd
import re

def extract_emails_from_profiles(usernames):
    # Creating an instance of the Instaloader class
    bot = instaloader.Instaloader()
    
    for username in usernames:
        try:
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

# Example usage
usernames = ['michaelbagebage', 'leomessi', 'cristiano']
extract_emails_from_profiles(usernames)
