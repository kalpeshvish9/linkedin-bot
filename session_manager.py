from dependencies import *

def get_session():
    if os.path.exists('linkedin_cookies.pkl'):
        driver = webdriver.Chrome()
        driver.get("https://www.linkedin.com")
        cookies = pickle.load(open("linkedin_cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get("https://www.linkedin.com")
        return driver
    else:
        driver = webdriver.Chrome()
        driver.get("https://www.linkedin.com/login")
        wait = WebDriverWait(driver, 10)
        username = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='session_key']")))
        username.send_keys(config.username)
        password = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='session_password']")))
        password.send_keys(config.password)
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit.click()
        pickle.dump(driver.get_cookies(), open("linkedin_cookies.pkl", "wb"))
        return driver