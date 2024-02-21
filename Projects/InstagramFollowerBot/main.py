import os

from instagram_bot import InstagramBot
from dotenv import load_dotenv

load_dotenv()

# Retrieve specific environment variables
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


def main():
    instagram_bot = InstagramBot()

    # Log in to Instagram
    instagram_bot.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

    # Navigate to a user
    instagram_bot.find_follower("nasa")

    # # Quit the driver
    instagram_bot.quit_driver()
    exit()


if __name__ == "__main__":
    main()
