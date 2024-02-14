import os
import requests
import time
import smtplib

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
}
PRODUCT_URL = "https://www.amazon.com/dp/B07YGZL8XF"
DEAL_PRICE = 199.99
# Path to the .env file for loading environment variables.
ENV_PATH = Path('..', '..', '.env')

# Load the .env file.
load_dotenv(dotenv_path=ENV_PATH)
# Retrieve specific environment variables.
mail_app_pass = os.getenv('MAIL_APP_PASS')
sender_email = os.getenv('MY_EMAIL')


def check_price():
    """
    Fetches the price of a product from a webpage.

    Returns:
        float: The price of the product, or None if the price cannot be fetched.
    """
    try:
        response = requests.get(PRODUCT_URL, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        price_whole = soup.find("span", class_="a-price-whole")
        price_fraction = soup.find("span", class_="a-price-fraction")

        if price_whole and price_fraction:
            price = f"{price_whole.get_text()}{price_fraction.get_text()}"
            return float(price)
    except requests.RequestException:
        print("Failed to fetch the webpage.")
        return None


def send_email(to, subject, content):
    """
    Sends an email using SMTP.

    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        content (str): The body content of the email.
    """
    # Connect to Gmail's SMTP server.
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # Secure the SMTP connection.
        connection.starttls()
        # Log in using the sender's credentials.
        connection.login(user=sender_email, password=mail_app_pass)
        # Send the email.
        connection.sendmail(
            from_addr=sender_email,
            to_addrs=to,
            msg=f"Subject:{subject}\n\n{content}",
        )


counter = 0
max_attempts = 15
current_price = check_price()

while current_price is None and counter < max_attempts:
    counter += 1
    print(f"Try #{counter}, returned: {current_price}")
    time.sleep(2)
    current_price = check_price()

if current_price is not None:
    if current_price > DEAL_PRICE:
        print("Today isn't the day to buy!")
    else:
        print("sending email")
        msg = f"Price is now ${current_price}! Buy now at {PRODUCT_URL}"
        send_email(
            to=sender_email,
            subject="Amazon Price Alert",
            content=f"Subject:BAXTOR - Amazon Price Watcher\n\n{msg}",
        )
    print(f"Bought at: ${DEAL_PRICE}\nCurrent: ${current_price}")
else:
    print("Sorry, please try again. I couldn't get the current price.")
