from dependencies import *
from session_manager import get_session
from selenium.webdriver.common.by import By

driver = get_session()

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")

username = wait.until(EC.presence_of_element_located((By.ID, "session_key")))
password = wait.until(EC.presence_of_element_located((By.ID, "session_password")))
submit_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sign-in-form__submit-button")))
submit_button.click()
