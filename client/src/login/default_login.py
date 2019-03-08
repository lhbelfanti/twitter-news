import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import constants
from config import DefaultConfiguration
from exceptions import LoadingTimeout
from logger import Logger
from login import Login


class DefaultLogin(Login):
    def __init__(self, driver, config):
        super().__init__(driver, config)
        Logger.info("Logging in...")

    def start(self):
        try:
            self.driver.wait_until_load(constants.PASSWORD_ELEMENT)
            self.login_user()
        except TimeoutException:
            raise LoadingTimeout()

    def login_user(self):
        # Getting form element
        form = self.driver.get_element(constants.FORM_ELEMENT)

        # Getting username and password input container
        username = form.get_element(constants.USERNAME_ELEMENT)
        password = form.get_element(constants.PASSWORD_ELEMENT)

        # Getting username and password input elements
        username_input = username.get_element(constants.LOGIN_INPUT_CLASS)
        password_input = password.get_element(constants.LOGIN_INPUT_CLASS)

        # Write username
        username_input.write(constants.USERNAME)

        # Sometimes the password is not written, so we wait 1 sec and then we write it
        time.sleep(self.config.get("wait_password"))

        # Write password
        password_input.write(constants.PASSWORD)

        # Click on submit button
        submit_button = form.get_element(constants.SUBMIT_FORM, By.CSS_SELECTOR)
        submit_button.click()

        Logger.info("Login success!")
        Logger.info("----------------------------------------")
