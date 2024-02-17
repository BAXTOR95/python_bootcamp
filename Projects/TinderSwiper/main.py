import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.common.action_chains import ActionChains

# Load environment variables from a .env file
from dotenv import load_dotenv

load_dotenv()

# Retrieve specific environment variables
FACEBOOK_EMAIL = os.getenv('FACEBOOK_EMAIL')
FACEBOOK_PASSWORD = os.getenv('FACEBOOK_PASSWORD')


def create_driver():
    """Create a Chrome WebDriver with options."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def sign_in(driver, email, password):
    """Sign in to the website using provided credentials."""
    try:
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Log in"))
        )
        login_button.click()

        # Log in with Facebook
        try:
            fb_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "[aria-label='Log in with Facebook']")
                )
            )
            fb_button.click()

            # Wait for the new window to appear
            WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

            # Simplified window handling
            base_window = driver.window_handles[0]
            fb_login_window = driver.window_handles[1]
            driver.switch_to.window(fb_login_window)

            # Fill in the Facebook login form
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            driver.find_element(By.NAME, value="email").send_keys(email)
            driver.find_element(By.NAME, value="pass").send_keys(password)
            driver.find_element(By.NAME, value="login").click()

            # Switch back to the main window
            driver.switch_to.window(base_window)

        except TimeoutException:
            print("No Facebook login button found or issue with window switching...")

    except TimeoutException:
        print("No login button found...")


def accept_cookies(driver):
    """Accept cookies on the website."""
    try:
        cookies_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//div[contains(text(), 'I accept')]]")
            )
        )
        cookies_button.click()
    except TimeoutException:
        print("No cookies button found...")


def allow_location(driver):
    """Allow location on the website."""
    try:
        location_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[aria-label='Allow']"))
        )
        location_button.click()
    except TimeoutException:
        print("No location button found...")


def turn_off_notifications(driver):
    """Turn off notifications on the website."""
    try:
        # Wait for either button to be clickable
        notification_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@aria-label, 'Not interested') or contains(@aria-label, 'I’ll miss out')]",
                )
            )
        )
        notification_button.click()
    except TimeoutException:
        print("No notification button found...")


def deny_premium(driver):
    """Deny premium on the website."""
    try:
        premium_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//div[contains(text(), 'Maybe Later')]]")
            )
        )
        premium_button.click()
    except TimeoutException:
        print("No premium button found...")


def reject_special_offer(driver):
    """Reject special offer on the website."""
    try:
        special_offer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(), 'Maybe Later')]]")
            )
        )
        special_offer_button.click()
    except TimeoutException:
        print("No special offer button found...")


def skip_sending_message(driver):
    """Skip sending a message to increase chances."""
    try:
        skip_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(), 'Skip')]]")
            )
        )
        skip_button.click()
        return True  # Indicate the button was found and clicked
    except TimeoutException:
        print("Skip button not found or not clickable.")
        return False  # Indicate the button was not found or clicked
    except NoSuchElementException:
        print("Skip button element not found.")
        return False  # Indicate the button was not found or clicked


def dismiss_add_tinder_to_home_screen(driver):
    """Dismiss the 'Add Tinder to Home Screen' prompt."""
    try:
        dismiss_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//div[contains(text(), 'Not interested')]]")
            )
        )
        dismiss_button.click()
        return True  # Indicate the button was found and clicked
    except TimeoutException:
        print("Dismiss button not found or not clickable.")
        return False  # Indicate the button was not found or clicked
    except NoSuchElementException:
        print("Dismiss button element not found.")
        return False  # Indicate the button was not found or clicked


def close_popup(driver):
    """Close a popup window."""
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-hidden='false']"))
        )
        # Scroll the button into view and attempt to click it
        driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
        time.sleep(1)  # Wait for any potential overlays to disappear
        close_button.click()
        print("Popup closed successfully.")
        return True  # Successfully closed the popup
    except TimeoutException:
        print("Close button not found or not clickable.")
        return False  # Popup not found or couldn't be closed
    except NoSuchElementException:
        print("Close button element not found.")
        return False  # Popup not found or couldn't be closed
    except ElementClickInterceptedException:
        # Use JavaScript click as a fallback
        driver.execute_script("arguments[0].click();", close_button)
        print("Popup closed using JavaScript.")
        return True  # Successfully closed the popup


def dismiss_all_requests(driver):
    """Dismiss all requests that might pop up."""
    accept_cookies(driver)
    allow_location(driver)
    turn_off_notifications(driver)
    deny_premium(driver)
    reject_special_offer(driver)


def click_back_to_tinder_button(driver):
    """Click the 'Back to Tinder' button after a match."""
    try:
        back_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[title='Back to Tinder']")
            )
        )
        back_button.click()
        return True  # Indicate the button was found and clicked
    except TimeoutException:
        print("Back to Tinder button not found or not clickable.")
        return False  # Indicate the button was not found or clicked
    except NoSuchElementException:
        print("Back to Tinder button element not found.")
        return False  # Indicate the button was not found or clicked


def swipe_right(driver):
    """Swipe right on a profile, and handle various scenarios."""
    match_handled = False  # Flag to indicate if a match was handled

    try:
        like_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[normalize-space(text())='Like']]")
            )
        )
        like_button.click()
    except (ElementClickInterceptedException, TimeoutException):
        print("Handling overlays or pop-ups...")

        # Attempt to handle various scenarios
        for handler in [
            click_back_to_tinder_button,
            skip_sending_message,
            dismiss_add_tinder_to_home_screen,
            close_popup,
        ]:
            try:
                if handler(driver):  # Check if the handler was successful
                    if (
                        handler.__name__ == "close_popup"
                    ):  # Check if the popup was successfully closed
                        print("Likely ran out of likes. Quitting driver.")
                        driver.quit()  # Quit the driver
                        exit()  # Exit the script
                    else:  # If the popup wasn't closed
                        match_handled = True  # Indicate a match or overlay was handled
                        break  # Exit the loop after handling
                else:
                    print(f"{handler.__name__} failed to handle the overlay.")
            except Exception as e:
                print(
                    f"Attempted action with {handler.__name__}, but encountered an issue: {e}"
                )

        if not match_handled:
            print("Could not handle the current page state. Please check manually.")

        # Random wait to mimic human behavior
        time.sleep(random.uniform(1, 3))


def main():
    driver = create_driver()
    driver.get("https://tinder.com/")

    sign_in(driver, FACEBOOK_EMAIL, FACEBOOK_PASSWORD)
    dismiss_all_requests(driver)

    while True:
        swipe_right(driver)
        time.sleep(1)


if __name__ == "__main__":
    main()
