import re
from data_manager import DataManager


def validate_email(email, confirm_email):
    """Validate if an email is valid and matches the confirm email."""
    if email == confirm_email:
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            print("That's not a real email. Please try again.")
            return False
    else:
        print("Emails do not match. Please try again.")
        return False


def ask_user_data():
    """Ask the user for their first name, last name, and email."""
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

    while True:
        email = input("Enter your email: ")
        confirm_email = input("Confirm your email: ")

        if validate_email(email, confirm_email):
            break

    return first_name, last_name, email


def validate_user_data(user_data, original_data):
    """Validate if the user data matches the original data."""
    return user_data == original_data


if __name__ == "__main__":
    first_name, last_name, email = ask_user_data()
    data_manager = DataManager()
    if data_manager.validate_if_email_exists(email):
        print("You're already in the club!")
        exit()

    data = data_manager.post_user_data(first_name, last_name, email)
    if validate_user_data(
        data, {"user": {"firstName": first_name, "lastName": last_name, "email": email}}
    ):
        print("Success! Your email has been added, look forward to working with you.")
    else:
        print("There was an error, please try again.")
