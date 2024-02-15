from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Keep Chrome browser open after running the script.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create a new instance of the Chrome browser
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a webpage
driver.get("https://en.wikipedia.org/wiki/Main_Page")

# Find element by CSS Selector
n_articles = driver.find_element(By.CSS_SELECTOR, value="#articlecount a")
# print(n_articles.text)
# n_articles.click()

# Find element by Link text
all_portals = driver.find_element(By.LINK_TEXT, value="Content portals")
# all_portals.click()

# Find the "Search" <input> by Name
search = driver.find_element(By.NAME, value="search")

# Sending keyboard input to Selenium
search.send_keys("Python", Keys.ENTER)

# driver.quit()
