import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import constants
from config import Configuration
from driver import Driver
from exceptions import LoadingTimeout
from logger import Logger
from login import Login


class DefaultLogin(Login):
    def __init__(self):
        super().__init__()
        self._driver = None
        self._config = None

    def _define_dependencies(self):
        self._add_dependency(Driver)
        self._add_dependency(Configuration)

    def construct(self, dependencies):
        self._driver = self._get_dependency(Driver, dependencies)
        self._config = self._get_dependency(Configuration, dependencies)

    def login_user(self):
        Logger.info("Logging in...")
        try:
            self._driver.wait_until_load(constants.PASSWORD_ELEMENT)
            self._login()
        except TimeoutException:
            raise LoadingTimeout()

    def _login(self):
        # Getting form element
        form = self._driver.get_element(constants.FORM_ELEMENT)

        # Getting username and password input container
        username = form.get_element(constants.USERNAME_ELEMENT)
        password = form.get_element(constants.PASSWORD_ELEMENT)

        # Getting username and password input elements
        username_input = username.get_element(constants.LOGIN_INPUT_CLASS)
        password_input = password.get_element(constants.LOGIN_INPUT_CLASS)

        # Write username
        username_input.write(constants.USERNAME)

        # Sometimes the password is not written, so we wait 1 sec and then we write it
        time.sleep(self._config.get("wait_password"))

        # Write password
        password_input.write(constants.PASSWORD)

        # Click on submit button
        submit_button = form.get_element(constants.SUBMIT_FORM, By.CSS_SELECTOR)
        submit_button.click()

        Logger.info("Login success!")
        Logger.info("----------------------------------------")
