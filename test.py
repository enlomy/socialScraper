import twint
import time

def scrape_twitter_profile(username):
    c = twint.Config()
    c.Username = username
    c.Store_object = True
    c.Hide_output = True

    retries = 3
    delay = 2

    while retries > 0:
        try:
            twint.run.Lookup(c)
            user = twint.output.users_list[0]

            # Extract user data
            full_name = user.name
            bio = user.bio
            location = user.location
            join_date = user.join_date

            # Print the scraped user data
            print("Username:", username)
            print("Full Name:", full_name)
            print("Bio:", bio)
            print("Location:", location)
            print("Join Date:", join_date)

            return
        except Exception as e:
            print("Failed to retrieve data from the profile.")
            print("Error:", str(e))

            retries -= 1
            if retries > 0:
                print("Retrying after", delay, "seconds...")
                time.sleep(delay)
                delay *= 2

    print("Max retries exceeded. Unable to scrape the profile.")

# Scrape user data from the provided Twitter profile
scrape_twitter_profile("LIndustries21")
