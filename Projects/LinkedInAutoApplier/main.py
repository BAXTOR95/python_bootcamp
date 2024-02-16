import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Load environment variables from a .env file
from dotenv import load_dotenv

load_dotenv()

# Retrieve specific environment variables
LINKEDIN_EMAIL = os.getenv('LINKEDIN_EMAIL')
LINKEDIN_PASSWORD = os.getenv('LINKEDIN_PASSWORD')


def create_driver():
    """Create a Chrome WebDriver with options."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def sign_in(driver, email, password):
    """Sign in to LinkedIn using provided credentials."""
    driver.find_element(By.LINK_TEXT, value="Sign in").click()
    driver.find_element(By.ID, value="username").send_keys(email)
    driver.find_element(By.ID, value="password").send_keys(password)
    driver.find_element(
        By.CSS_SELECTOR, value=".login__form_action_container button"
    ).click()


def scroll_into_view(driver, element):
    """Scrolls the page until the element is in the viewport."""
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()


def apply_to_jobs(driver):
    """Iterate through job listings and attempt to apply."""
    job_list = driver.find_elements(
        By.CSS_SELECTOR, value=".jobs-search-results__list-item"
    )

    for job_posting in job_list:
        scroll_into_view(driver, job_posting)
        try:
            # Wait for the link inside the job posting to be present
            job_posting_title_element = WebDriverWait(job_posting, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "a"))
            )
            job_posting_title = job_posting_title_element.text
            print(f"Attempting to apply for '{job_posting_title}' job posting...")
            job_posting.click()

            # Wait for the apply button to be clickable
            try:
                apply_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(@aria-label, 'Easy Apply') and contains(@class, 'jobs-apply-button')]",
                        )
                    )
                )
                apply_button.click()

                # Attempt to submit the application
                try:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "[aria-label='Submit application']")
                        )
                    )
                    next_button.click()

                    # Wait for the confirmation modal to appear and dismiss it
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located(
                                (By.CSS_SELECTOR, ".artdeco-modal__dismiss")
                            )
                        )
                        time.sleep(5)  # Ensure we wait at least 5 seconds
                        driver.find_element(
                            By.CSS_SELECTOR, value=".artdeco-modal__dismiss"
                        ).click()
                    except TimeoutException:
                        print(
                            "Confirmation modal did not appear within the expected time."
                        )

                except TimeoutException:
                    print("No submit application button found. Skipping...")
                    # Close any modal that might have appeared
                    try:
                        driver.find_element(
                            By.CSS_SELECTOR, value=".artdeco-modal__dismiss"
                        ).click()
                        driver.find_element(
                            By.CSS_SELECTOR, value=".artdeco-modal__confirm-dialog-btn"
                        ).click()
                    except NoSuchElementException:
                        print("Failed to close the modal, element not found.")

            except (NoSuchElementException, TimeoutException):
                print("No Easy Apply button found or already applied. Skipping...")
        except TimeoutException:
            print("Timed out waiting for job posting link to be present.")
        except NoSuchElementException:
            print("Job posting link not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def apply_to_all_jobs(driver):
    """Apply to jobs across all available pages."""
    while True:
        try:
            # Wait for the job listings to load on the current page
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, ".jobs-search-results__list-item")
                )
            )
            apply_to_jobs(driver)

        except TimeoutException:
            # If no job listings are found, we've reached the end or an empty page
            print(
                "No more job listings found on the next page. Ending application process."
            )
            break

        # Re-fetch the pagination elements to avoid stale element references
        try:
            pagination_ul = driver.find_element(
                By.CSS_SELECTOR, ".jobs-search-results-list__pagination ul"
            )
            pages_li = pagination_ul.find_elements(By.TAG_NAME, "li")

            # Find the current active page
            active_page = pagination_ul.find_element(By.CSS_SELECTOR, "li.active")
            active_page_index = pages_li.index(active_page)

            # Check if the current page is the last page
            if active_page_index >= len(pages_li) - 1:
                print("Reached the last page of job listings.")
                break

            # Move to the next page
            next_page_li = pages_li[active_page_index + 1]
            next_page_li.click()
            # Wait for a brief moment to allow the page to start loading
            time.sleep(2)

        except NoSuchElementException:
            # If pagination elements are not found, it means we've reached the last page
            print("Pagination not found, might be on the last page.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


def main():
    driver = create_driver()
    driver.get(
        "https://www.linkedin.com/jobs/search/?currentJobId=3820843798&distance=50&f_AL=true&geoId=105142029&keywords=python%20developer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R"
    )

    sign_in(driver, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    time.sleep(5)  # Wait for the sign-in process to complete and the page to load
    apply_to_all_jobs(driver)

    driver.quit()


if __name__ == "__main__":
    main()
