import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from decorators import version1, version2
import constants
from exceptions import LoadingTimeout


class TrendFilter:
    def __init__(self, driver, config, trend):
        self._driver = driver
        self._config = config
        self._trend = trend
        self.stream_items = None

    def start(self, open_url=True):
        self._add_filters_to_url()

        # Opening trend
        if open_url:
            self._driver.navigate_to(self._trend.url)

        try:
            st_it = self._get_stream_items_v1()
            self.stream_items = self._get_stream_items_v2() if st_it is None else st_it
            time.sleep(self._config.get_prop("wait_page_load", constants.DE_CFG))
        except TimeoutException:
            raise LoadingTimeout()

    @version1
    def _get_stream_items_v1(self):
        return self._driver.wait_until_load(self._config.get_prop("tweets_list"))

    @version2
    def _get_stream_items_v2(self):
        return self._driver.wait_until_load(self._config.get_prop("tweets_list"), By.CSS_SELECTOR)

    @version1
    def _add_filters_to_url(self):
        # Adding default filter: ?vertical=default
        self._trend.url += self._config.get_prop("default_filter")
        # Adding location filter: &near=me
        # self.trend.url += self._config.get_prop("location_filter") # Need to handle when there isn't any tweet
        # Adding language filter: &l=es
        self._trend.url += self._config.get_prop("language_filter")
