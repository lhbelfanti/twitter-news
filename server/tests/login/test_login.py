import unittest

from unittest.mock import MagicMock, Mock, patch

from driver import TwitterDriver
from exceptions import LoadingTimeout
from login import DefaultLogin


class LoginTest(unittest.TestCase):
    def setUp(self):
        # Create Driver
        self._driver = TwitterDriver()
        attrs = {'get.return_value': 0}
        config_mock = MagicMock(**attrs)
        self._driver.config = config_mock
        self._driver.create_driver()
        # Create Login
        self._login = DefaultLogin()
        self._login._driver = self._driver
        self._login._config = config_mock

    @patch("logger.Logger.info", return_value="")
    @patch("driver.TwitterDriver.wait_until_load", Mock())
    @patch("constants.USERNAME", "user")
    @patch("constants.PASSWORD", "pass")
    def test_should_authenticate_user(self, logger_mock):
        self._login._get_form_elements = Mock()
        user_input_mock = Mock()
        password_input_mock = Mock()
        button_mock = Mock()
        self._login._username_input = user_input_mock
        self._login._password_input = password_input_mock
        self._login._submit_button = button_mock
        self._login.authenticate()
        user_input_mock.write.assert_called_once_with("user")
        password_input_mock.write.assert_called_once_with("pass")
        button_mock.click.assert_called_once()

    @patch("logger.Logger.info", return_value="")
    def test_should_throw_timeout_exception(self, logger_mock):
        with self.assertRaises(LoadingTimeout) as cm:
            self._login.authenticate()
        print(cm.exception.args[0])

    def tearDown(self):
        self._driver.close()
        self._login = None
