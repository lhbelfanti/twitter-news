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
        self._username_input = None
        self._password_input = None
        self._submit_button = None

    def _define_dependencies(self):
        self._add_dependency(Driver)
        self._add_dependency(Configuration)

    def construct(self, dependencies):
        self._driver = self._get_dependency(Driver, dependencies)
        self._config = self._get_dependency(Configuration, dependencies)

    def authenticate(self):
        Logger.info("Logging in...")
        try:
            self._driver.wait_until_load(self._config.get_prop("password_element"))
            self._get_form_elements()
            self._login()
        except TimeoutException:
            raise LoadingTimeout()

    def _get_form_elements(self):
        # Getting form element
        form = self._driver.get_element(self._config.get_prop("form_element"))

        # Getting username and password input container
        username = form.get_element(self._config.get_prop("username_element"))
        password = form.get_element(self._config.get_prop("password_element"))

        # Getting username and password input elements
        self._username_input = username.get_element(self._config.get_prop("login_input_class"))
        self._password_input = password.get_element(self._config.get_prop("login_input_class"))
        self._submit_button = form.get_element(self._config.get_prop("submit_form"), By.CSS_SELECTOR)

    def _login(self):
        # Write username
        self._username_input.write(constants.USERNAME)

        # Sometimes the password is not written, so we wait 1 sec and then we write it
        time.sleep(self._config.get_prop("wait_password", constants.DE_CFG))

        # Write password
        self._password_input.write(constants.PASSWORD)

        # Click on submit button
        self._submit_button.click()

        Logger.info("Login success!")
        Logger.info("----------------------------------------")
