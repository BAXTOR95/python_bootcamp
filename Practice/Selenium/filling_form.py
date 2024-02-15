from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after running the script.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create a new instance of the Chrome browser
driver = webdriver.Chrome(options=chrome_options)

# Navigate to a webpage
driver.get("http://secure-retreat-92358.herokuapp.com")

# Find the first name input field
first_name = driver.find_element(By.NAME, value="fName")
first_name.send_keys("John")

# Find the last name input field
last_name = driver.find_element(By.NAME, value="lName")
last_name.send_keys("Doe")

# Find the email input field
email = driver.find_element(By.NAME, value="email")
email.send_keys("john.doe@gmail.com")

# Find the sign up button
sign_up_button = driver.find_element(By.TAG_NAME, value="button")
sign_up_button.click()

driver.quit()
