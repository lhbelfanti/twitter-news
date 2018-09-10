import constants
from selenium.webdriver.common.by import By


class Login:
    def __init__(self, driver):
        self.driver = driver

    def login_user(self):
        # Getting form element
        form = self.driver.find_element(By.CLASS_NAME, constants.FORM_ELEMENT)

        # Getting username and password input container
        username = form.find_element(By.CLASS_NAME, constants.USERNAME_ELEMENT)
        password = form.find_element(By.CLASS_NAME, constants.PASSWORD_ELEMENT)

        # Getting username and password input elements
        username_input = username.find_element(By.CLASS_NAME, constants.LOGIN_INPUT_CLASS)
        password_input = password.find_element(By.CLASS_NAME, constants.LOGIN_INPUT_CLASS)

        # Write username and password
        username_input.send_keys(constants.USERNAME)
        password_input.send_keys(constants.PASSWORD)

        # Click on submit button
        submit_button = form.find_element(By.CSS_SELECTOR, constants.SUBMIT_FORM)
        submit_button.click()
