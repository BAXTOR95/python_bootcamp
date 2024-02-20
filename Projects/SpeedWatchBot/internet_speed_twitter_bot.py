import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class InternetSpeedTwitterBot:

    def __init__(self):
        self.up = 0.00
        self.down = 0.00
        self.ping = 0.00
        self.PROMISED_DOWN = 300.00
        self.PROMISED_UP = 10.00
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def get_internet_speed(self):
        """Run a speed test and return the results."""
        # Open the speed test website
        self.driver.get("https://www.speedtest.net/")

        # Click the "Go" button to start the test
        go_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "js-start-test"))
        )
        go_button.click()

        # Wait for the test to complete and the results to be available
        WebDriverWait(self.driver, 120).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "eot-info-audience"))
        )

        # Close any pop up ads
        try:
            close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Close')]")
                )
            )
            close_button.click()
        except (NoSuchElementException, TimeoutException):
            pass

        # Get the results
        self.down = float(
            self.driver.find_element(By.CLASS_NAME, "download-speed").text
        )
        self.up = float(self.driver.find_element(By.CLASS_NAME, "upload-speed").text)
        self.ping = float(self.driver.find_element(By.CLASS_NAME, "ping-speed").text)

    def login(self, email, password):
        """Sign in to Twitter using provided credentials."""
        # Open the Twitter login page
        self.driver.get("https://twitter.com/login")

        # Fill in the login username/mail and click next
        email_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_field.send_keys(email)
        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Next']/ancestor::div[@role='button']")
            )
        )
        next_button.click()

        # Fill in the password and click login
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Log in']/ancestor::div[@role='button']")
            )
        )
        login_button.click()

        # Wait until you successfully get to the home page
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_to_be("https://twitter.com/home"))

    def tweet_at_provider(self):
        """Tweet at the internet provider with the current internet speed."""
        # Compose the tweet
        tweet_text = f"Hey @Ask_Spectrum, why is my internet speed {self.down} down/{self.up} up when I pay for {self.PROMISED_DOWN} down/{self.PROMISED_UP} up?"

        # Open the Twitter compose tweet page
        self.driver.get("https://twitter.com/compose/tweet")

        # Wait for the tweet text area to be present
        tweet_text_area = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[aria-label='Post text']")
            )
        )
        tweet_text_area.send_keys(tweet_text)

        # Click the tweet button
        tweet_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='Post']/ancestor::div[@role='button']")
            )
        )
        tweet_button.click()

    def speeds_as_promised(self):
        """Check if the internet speeds are as promised"""
        if self.down < self.PROMISED_DOWN or self.up < self.PROMISED_UP:
            print("Speeds are below promised...")
            return False
        else:
            print("Speeds are as promised.")
            return True

    def quit_driver(self):
        """Close the Chrome driver."""
        self.driver.quit()
        print("Driver closed.")
