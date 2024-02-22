import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


class DataEntryBot:
    """
    Class to automate data entry on a research form using Selenium.
    """

    def __init__(self):
        """
        Initialize the DataEntryBot.
        """
        load_dotenv()
        # edit form at https://docs.google.com/forms/u/0/
        self.RESEARCH_FORM_LINK = os.getenv("RESEARCH_FORM_LINK")
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def fill_form(self, address, price, link):
        """
        Fill in the form with the provided data.

        Args:
            address (str): The address to fill in the form.
            price (str): The price to fill in the form.
            link (str): The link to the property to fill in the form.
        """
        try:
            self.driver.get(self.RESEARCH_FORM_LINK)
            # Set up WebDriverWait
            wait = WebDriverWait(self.driver, 10)  # 10 seconds timeout

            # Wait for and fill the address input
            address_input = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[aria-labelledby="i1"]')
                )
            )
            address_input.send_keys(address)

            # Wait for and fill the price per month input
            price_input = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[aria-labelledby="i5"]')
                )
            )
            price_input.send_keys(price)

            # Wait for and fill the link to the property input
            link_input = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'input[aria-labelledby="i9"]')
                )
            )
            link_input.send_keys(link)

            # Click the submit button
            submit_button = self.driver.find_element(
                By.CSS_SELECTOR, "div[role='button']"
            )
            submit_button.click()

        except Exception as e:
            print(f"An error occurred while filling the form: {e}")

    def quit(self):
        """
        Close the Chrome WebDriver.
        """
        self.driver.quit()
