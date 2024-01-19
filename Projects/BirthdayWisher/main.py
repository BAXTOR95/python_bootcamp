import os
import pandas as pd
import datetime as dt
import smtplib
import random
import pytz
from dotenv import load_dotenv
from pathlib import Path

# -------------------------------- CONSTANTS -------------------------------- #
# Path to the folder containing letter templates.
TEMPLATES = "./letter_templates"
# Path to the .env file for loading environment variables.
ENV_PATH = Path('..', '..', '.env')

# -------------------------------- VARIABLES -------------------------------- #
# List to store birthday data loaded from CSV.
birthdays = []
# Stores the app-specific password for email access.
mail_app_pass = ""
# Stores the sender's email address.
sender_email = ""


# ------------------------------- FUNCTIONS --------------------------------- #
def get_random_template():
    """
    Selects a random letter template file and returns its contents.

    Returns:
        str: The content of a randomly selected letter template.
    """
    # List all template files in the directory.
    templates = os.listdir(TEMPLATES)

    # Randomly select a template file.
    selected_template = random.choice(templates)

    # Construct the full path to the selected template.
    template_path = os.path.join(TEMPLATES, selected_template)

    # Read and return the contents of the selected template.
    with open(template_path, 'r') as file:
        return file.read()


def load_data():
    """
    Loads birthday data from a CSV file into a global list.
    """
    global birthdays
    # Read birthday data from CSV and convert to a list of dictionaries.
    data = pd.read_csv("birthdays.csv")
    birthdays = data.to_dict(orient="records")


def load_env():
    """
    Loads environmental variables from the .env file.
    """
    global mail_app_pass, sender_email
    # Load the .env file.
    load_dotenv(dotenv_path=ENV_PATH)
    # Retrieve specific environment variables.
    mail_app_pass = os.getenv('MAIL_APP_PASS')
    sender_email = os.getenv('MY_EMAIL')


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


def wish_happy_birthday():
    """
    Checks for today's birthdays and sends out emails.
    """
    # Get's today's date in ETS timezone
    tz = pytz.timezone('EST')
    now = dt.datetime.now(tz)
    # Process each birthday in the list.
    if len(birthdays) > 0:
        for birthday in birthdays:
            # Format today's date and birthday date for comparison.
            birthday_date = f"{birthday['month']}/{birthday['day']}"
            current_date = f"{now.month}/{now.day}"
            # Check if today is someone's birthday.
            if current_date == birthday_date:
                # Generate a personalized birthday letter.
                letter = get_random_template().replace("[NAME]", birthday['name'])
                # Send the birthday email.
                send_email(birthday["email"], "Happy Birthday!", letter)


# ---------------------------------- MAIN ----------------------------------- #
# Initial setup: Load data and environment variables.
load_data()
load_env()

# Execute the main functionality: Send birthday emails.
wish_happy_birthday()