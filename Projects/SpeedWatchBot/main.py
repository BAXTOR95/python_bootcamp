import os
from internet_speed_twitter_bot import InternetSpeedTwitterBot

# Load environment variables from a .env file
from dotenv import load_dotenv

load_dotenv()

# Retrieve specific environment variables
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")


def main():
    twitter_bot = InternetSpeedTwitterBot()

    # Get the internet speed and tweet at the provider if the speeds are not as promised
    twitter_bot.get_internet_speed()
    if not twitter_bot.speeds_as_promised():
        twitter_bot.login(TWITTER_USERNAME, TWITTER_PASSWORD)
        twitter_bot.tweet_at_provider()

    # Quit the driver
    twitter_bot.quit_driver()
    exit()


if __name__ == "__main__":
    main()
