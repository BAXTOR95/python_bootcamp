import time
from selenium import webdriver
from selenium.webdriver.common.by import By

UPGRADE_CHECK_INTERVAL = 5  # seconds
GAME_STOP_TIME = 5 * 60  # seconds


def create_driver():
    """Creates and returns a Chrome WebDriver with options to keep the browser open."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    return webdriver.Chrome(options=chrome_options)


def click_cookie(driver):
    """Finds and clicks the cookie."""
    driver.find_element(By.ID, value="cookie").click()


def get_current_cookies(driver):
    """Returns the current number of cookies as an integer."""
    return int(driver.find_element(By.ID, value="money").text.replace(",", ""))


def buy_best_upgrade(driver, current_cookies):
    """Finds and clicks the best affordable upgrade based on current cookies."""
    store = driver.find_element(By.ID, value="store")
    items = store.find_elements(By.XPATH, "./div")

    affordable_upgrades = []
    for item in items:
        if "grayed" not in item.get_attribute("class"):
            b_tag = item.find_element(By.TAG_NAME, "b")
            # Assuming price is always the last element after splitting by space and removing commas
            b_value = int(b_tag.text.split()[-1].replace(",", ""))
            if b_value <= current_cookies:
                affordable_upgrades.append((item, b_value))

    if affordable_upgrades:
        best_upgrade = max(affordable_upgrades, key=lambda x: x[1])
        best_upgrade_element = best_upgrade[0]
        best_upgrade_element.click()


def get_cookies_second(driver):
    """Returns the current number of cookies per second as a float."""
    return float(driver.find_element(By.ID, value="cps").text.split()[-1])


def main():
    driver = create_driver()
    driver.get("https://orteil.dashnet.org/experiments/cookie/")

    start_time = time.time()
    upgrade_check_time = start_time

    while True:
        click_cookie(driver)

        current_time = time.time()
        elapsed_time = current_time - start_time
        time_since_last_check = current_time - upgrade_check_time

        # Every 5 seconds, attempt to buy an upgrade
        if time_since_last_check >= 5:
            current_cookies = get_current_cookies(driver)
            buy_best_upgrade(driver, current_cookies)
            upgrade_check_time = current_time  # Reset the upgrade check time

        # After 5 minutes, print the current cookie count, stop the loop, and close the driver
        if elapsed_time >= GAME_STOP_TIME:
            final_cookies_second = get_cookies_second(driver)
            print(f"cookies/second: {final_cookies_second}")
            break

    driver.quit()


if __name__ == "__main__":
    main()
