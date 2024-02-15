from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after running the script.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
# driver.get("https://www.amazon.com/dp/B07YGZL8XF?th=1")

# driver.implicitly_wait(10)

# price_whole = driver.find_element(By.CLASS_NAME, value="a-price-whole")
# price_fraction = driver.find_element(By.CLASS_NAME, value="a-price-fraction")
# print(f"The price is: {price_whole.text}.{price_fraction.text}")

driver.get("https://www.python.org/")

# search_bar = driver.find_element(By.NAME, value="q")
# # print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))
# button = driver.find_element(By.ID, value="submit")
# print(button.size)
# documentation_link = driver.find_element(
#     By.CSS_SELECTOR, value=".documentation-widget a"
# )
# print(documentation_link.text)

# bug_link = driver.find_element(
#     By.XPATH, value='//*[@id="site-map"]/div[2]/div/ul/li[3]/a'
# )
# print(bug_link.text)

# driver.find_elements(By.CSS_SELECTOR, value="")

# Grabbing the container for upcoming events
# upcoming_events = driver.find_elements(
#     By.XPATH, value='//*[@id="content"]/div/section/div[2]/div[2]/div/ul/li'
# )
upcoming_events = driver.find_elements(By.CSS_SELECTOR, value=".event-widget ul li")

events = {}

# Loop through each event
for event in upcoming_events:
    # Find the 'time' element within each event
    time_element = event.find_element(By.TAG_NAME, 'time')

    # Find the 'a' element (link) within each event
    link_element = event.find_element(By.TAG_NAME, 'a')

    events[time_element.text] = {
        "title": link_element.text,
        "link": link_element.get_attribute('href'),
    }

print(events)

# driver.close()
driver.quit()
