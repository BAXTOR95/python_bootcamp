import os
import smtplib

from dotenv import load_dotenv
from pathlib import Path
from twilio.rest import Client


class NotificationManager:
    """This class is responsible for sending notifications with the deal flight details."""

    def __init__(self) -> None:
        self.ENV_PATH = Path("..", "..", ".env")
        load_dotenv(dotenv_path=self.ENV_PATH)
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, message: str):
        """Send an SMS with the given message.

        Args:
            message (str): The message to send.
        """
        message = self.client.messages.create(
            body=message,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            to=os.getenv("MY_PHONE_NUMBER"),
        )
        print(message.sid)

    def send_email(self, message: str, email: str):
        """Send an email with the given message.

        Args:
            message (str): The message to send.
            email (str): The email to send the message to.
        """
        pass
        # Implement email sending here
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(
                user=os.getenv("MY_EMAIL"), password=os.getenv("MAIL_APP_PASS")
            )
            connection.sendmail(
                from_addr=os.getenv("MY_EMAIL"),
                to_addrs=email,
                msg=f"Subject:Low price alert!\n\n{message}",
            )
