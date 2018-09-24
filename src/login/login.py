import constants
import utils
import time
from exceptions import LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class Login:
    def __init__(self, driver):
        self.driver = driver

    def start(self):
        try:
            utils.wait_until_load(By.CLASS_NAME, constants.PASSWORD_ELEMENT, self.driver)
            self.login_user()
        except TimeoutException:
            raise LoadingTimeout()

    def login_user(self):
        # Getting form element
        form = utils.get_element_by(By.CLASS_NAME, constants.FORM_ELEMENT, self.driver)

        # Getting username and password input container
        username = utils.get_element_by(By.CLASS_NAME, constants.USERNAME_ELEMENT, form)
        password = utils.get_element_by(By.CLASS_NAME, constants.PASSWORD_ELEMENT, form)

        # Getting username and password input elements
        username_input = utils.get_element_by(By.CLASS_NAME, constants.LOGIN_INPUT_CLASS, username)
        password_input = utils.get_element_by(By.CLASS_NAME, constants.LOGIN_INPUT_CLASS, password)

        # Write username and password
        username_input.send_keys(constants.USERNAME)
        time.sleep(1)  # Sometimes the password is not written, so we wait 1 sec and then we write it
        password_input.send_keys(constants.PASSWORD)

        # Click on submit button
        submit_button = utils.get_element_by(By.CSS_SELECTOR, constants.SUBMIT_FORM, form)
        submit_button.click()

        print("Login success!")
