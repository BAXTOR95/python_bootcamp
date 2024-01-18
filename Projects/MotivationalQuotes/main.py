import datetime as dt
import os
import smtplib
import random
from dotenv import load_dotenv
from pathlib import Path


def get_random_quote():
    """Returns random quote"""
    with open("quotes.txt") as file:
        quotes = [line.strip() for line in file.readlines()]
        return random.choice(quotes)


# Path to the directory containing the .env file
env_path = Path('..', '..', '.env')

# Load the .env file
load_dotenv(dotenv_path=env_path)

# Access the environment variable
mail_app_pass = os.getenv('MAIL_APP_PASS')
my_email = os.getenv('MY_EMAIL')
# receiver_email = os.getenv('RECEIVER_EMAIL')

# Get day of the week
now = dt.datetime.now()
weekday = now.weekday()

if weekday == 0:  # If its wednesday, send the motivational email
    # Start the SMTP connection
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Secure the connection
        connection.starttls()
        # Log in
        connection.login(user=my_email, password=mail_app_pass)
        # Send email
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Quote of the Week!\n\n{get_random_quote()}",
        )
