from dependencies import *
from session_manager import get_session
from selenium.webdriver.common.by import By

driver = get_session()

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com")

username = driver.find_element(By.ID, "session_key")
username.send_keys(config.username)
password = driver.find_element_by_id("session_password")
password.send_keys(config.password)
driver.find_element_by_class_name("sign-in-form__submit-button").click()
