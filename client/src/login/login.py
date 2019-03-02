import constants
import time
from driver import WebDriverUtils as Utils
from config import Configuration
from exceptions import LoadingTimeout
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from logger import Logger


class Login:
    def __init__(self, driver):
        self.driver = driver
        self.utils = Utils()

    def start(self):
        try:
            self.utils.wait_until_load(By.CLASS_NAME, constants.PASSWORD_ELEMENT, self.driver)
            self.login_user()
        except TimeoutException:
            raise LoadingTimeout()

    def login_user(self):
        # Getting form element
        form = self.utils.get_element_by(By.CLASS_NAME, constants.FORM_ELEMENT, self.driver)

        # Getting username and password input container
        username = self.utils.get_element_by(By.CLASS_NAME, constants.USERNAME_ELEMENT, form)
        password = self.utils.get_element_by(By.CLASS_NAME, constants.PASSWORD_ELEMENT, form)

        # Getting username and password input elements
        username_input = self.utils.get_element_by(By.CLASS_NAME, constants.LOGIN_INPUT_CLASS, username)
        password_input = self.utils.get_element_by(By.CLASS_NAME, constants.LOGIN_INPUT_CLASS, password)

        # Write username and password
        username_input.send_keys(constants.USERNAME)
        # Sometimes the password is not written, so we wait 1 sec and then we write it
        time.sleep(Configuration.config["wait_password"])
        password_input.send_keys(constants.PASSWORD)

        # Click on submit button
        submit_button = self.utils.get_element_by(By.CSS_SELECTOR, constants.SUBMIT_FORM, form)
        submit_button.click()

        Logger.info("Login success!")
