import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class InstagramBot:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get("https://www.instagram.com/")

    def login(self, username, password):
        """Log in to Instagram using provided credentials."""
        # Fill in the login username/mail and click next
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_input.send_keys(username)
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(password)
        password_input.submit()
        self.reject_save_login_info()
        self.reject_notifications()

    def reject_save_login_info(self):
        """Reject the 'Save Login Info' prompt."""
        not_now_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and contains(text(), 'Not now')]")
            )
        )
        not_now_button.click()

    def reject_notifications(self):
        """Reject the 'Turn on Notifications' prompt."""
        not_now_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Not Now')]")
            )
        )
        not_now_button.click()

    def scroll_into_view(self, driver, element):
        """Scrolls the page until the element is in the viewport."""
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()

    def follow_followers(self):
        """Follow all the followers of a user."""
        followers_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@href, '/followers/')]")
            )
        )
        followers_button.click()
        time.sleep(2)
        follow_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//div[text()='Follow']/ancestor::button")
            )
        )
        for button in follow_buttons:
            self.scroll_into_view(self.driver, button)
            button.click()
            time.sleep(random.randint(1, 3))

    def find_follower(self, username):
        """Find a user's profile and follow them."""
        self.driver.get(f"https://www.instagram.com/{username}/")
        try:
            follow_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[text()='Follow']/ancestor::button")
                )
            )
            follow_button.click()
        except (NoSuchElementException, TimeoutException):
            print(f"You are already following {username}.")
        else:
            print(f"You are now following {username}.")

        # Follow all the followers of the user
        self.follow_followers()

    def quit_driver(self):
        """Quit the WebDriver."""
        self.driver.quit()
