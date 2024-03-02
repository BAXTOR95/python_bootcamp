import os
import smtplib

from dotenv import load_dotenv
from twilio.rest import Client


class NotificationManager:
    """This class is responsible for sending notifications."""

    def __init__(self) -> None:
        load_dotenv()
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

    def send_email(self, form_data: dict, recipient_email: str):
        """Send an email using form data.

        Args:
            form_data (dict): The form data containing name, email, phone, and message.
            recipient_email (str): The recipient's email address.
        """
        subject = "New Contact Submission"
        body = (
            f"Name: {form_data.get('name')}\n"
            f"Email: {form_data.get('email')}\n"
            f"Phone: {form_data.get('phone')}\n"
            f"Message: {form_data.get('message')}"
        )
        email_message = f"Subject: {subject}\n\n{body}"

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(
                user=os.getenv("MY_EMAIL"), password=os.getenv("MAIL_APP_PASS")
            )
            connection.sendmail(
                from_addr=os.getenv("MY_EMAIL"),
                to_addrs=recipient_email,
                msg=email_message,
            )
